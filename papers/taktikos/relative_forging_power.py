import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.widgets import Button
import multiprocessing as mp
from matplotlib.widgets import AxesWidget, RadioButtons
from scipy import interpolate
from scipy import signal
from collections import defaultdict


# Maximum value of gamma to be plotted
gamma_max = 100
# Truncation error in distribution summation as slot-interval diverges
trunc_error = 1.0e-6
#  Max number of iterations for convergent series
max_iter = 10000
# Number of nonces that the grinding simulation runs over
total_slots = 1000000
# Slot axis for grinding simulation
slots = np.arange(total_slots)
# Nonces for grinding simulation
ys = np.random.rand(total_slots)
# Number of generations to keep in branch reserve below the maximum generation (max block number)
branch_depth = 2
# Grid resolution for 3d surface plot
nx, ny = (10, 10)
# Number of data points for consistency contour
n_cons_plt = gamma_max
# Target chain growth for heatmap series over varying gamma and fa
target_f_eff = 0.075

# Initial Snowplow curve params
gamma_init = 15
fa_init = 0.5
fb_init = 0.05
slot_gap_init = 0

# Active stake scale factor (for reproducing honest distribution with (stake_scale*100)% active stake)
# This caps the adversarial stake as well, corresponding to a situation where (1.0 - stake_scale) is inactive
# e.g. if stake_scale is 0.2 then there is only 20% of all stake split across honest and adversarial parties
stake_scale = 1.0
init_stake = 1.0

plot_data = False
dataFileName = "test_threshold.txt"


# Initial delay value \Delta in semi-synchronous delay model
delay_init = 0

# Will use Proof-of-Work model instead if true
use_pow_test = False
# Use grinding simulation in heatmap calculation
heatmap_grind = False
# Numerical method used in probability density function calculation
numerical_method = "pi norm"
# Use a specified difficulty curve from txt
user_defined_curve = False


# Domain of slot intervals in all calculations
delta_axis = np.arange(0, gamma_max + 1)
# Domain of normalized resources r = (r_h/(r_a+r_h) = 1.0 - r_a/(r_a+r_h)
r_axis = np.linspace(0.0, 1.0, 20)

# User defined curve TODO add txt file input
l = 10
# difficulty_curve = np.sqrt(delta_axis)*0.01
# difficulty_curve = delta_axis*delta_axis*0.0005
# difficulty_curve = (signal.sawtooth(2 * np.pi * 0.1 * delta_axis) + 1.0) / 2.0
difficulty_curve = np.mod(delta_axis, l)/float(l-1)

# Settlement depth for plotting
k_settle = 10

# Proof-of-Work consistency bound, approximation of consistency bound derived from
# https://doi.org/10.1145/3372297.3423365
# Serves as baseline of comparison for numerical techniques as well as Proof-of-Stake vs Proof-of-Work


def pow_bound(x):
    if x > 0.0:
        return 0.5 + (2.0 - np.sqrt(x * x + 4.0)) / (2.0 * x)
    else:
        return 0.5


v_pow_bound = np.vectorize(pow_bound)


def log_power(arg1, arg2):
    if arg1*arg2 <= 0.0:
        return float('nan')
    elif arg1 > arg2:
        return np.log10(np.power(4*arg1*arg2, k_settle))
    else:
        return 0.0


v_log_power = np.vectorize(log_power)


def settlement_argument(f_eff_a, f_eff_h):
    prob_a = np.asarray(f_eff_a)/(np.asarray(f_eff_a) + np.asarray(f_eff_h))
    prob_h = np.asarray(f_eff_h)/(np.asarray(f_eff_a) + np.asarray(f_eff_h))
    return v_log_power(prob_h, prob_a)


class MyRadioButtons(RadioButtons):

    def __init__(self, ax, labels, active=0, activecolor='blue', size=49,
                 orientation="vertical", **kwargs):
        """
        Add radio buttons to an `~.axes.Axes`.
        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The axes to add the buttons to.
        labels : list of str
            The button labels.
        active : int
            The index of the initially selected button.
        activecolor : color
            The color of the selected button.
        size : float
            Size of the radio buttons
        orientation : str
            The orientation of the buttons: 'vertical' (default), or 'horizontal'.
        Further parameters are passed on to `Legend`.
        """
        AxesWidget.__init__(self, ax)
        self.activecolor = activecolor
        axcolor = ax.get_facecolor()
        self.value_selected = None

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        circles = []
        for i, label in enumerate(labels):
            if i == active:
                self.value_selected = label
                facecolor = activecolor
            else:
                facecolor = axcolor
            p = ax.scatter([], [], s=size, marker="o", edgecolor='black',
                           facecolor=facecolor)
            circles.append(p)
        if orientation == "horizontal":
            kwargs.update(ncol=len(labels), mode="expand")
        kwargs.setdefault("frameon", False)
        self.box = ax.legend(circles, labels, loc="center", **kwargs)
        self.labels = self.box.texts
        self.circles = self.box.legendHandles
        for c in self.circles:
            c.set_picker(5)
        # self.cnt = 0
        # self.observers = {}

        self.connect_event('pick_event', self._clicked)

    def _clicked(self, event):
        if (self.ignore(event) or event.mouseevent.button != 1 or
                event.mouseevent.inaxes != self.ax):
            return
        if event.artist in self.circles:
            self.set_active(self.circles.index(event.artist))


# Difficulty curve
def f(delta, gamma, slot_gap, fa, fb):
    if delta <= slot_gap:
        return 0.0
    elif delta <= gamma:
        if user_defined_curve:
            return min(1.0, fa * difficulty_curve[delta])
        else:
            # default snowplow curve
            return min(1.0, fa * (float(delta - slot_gap)) / float(gamma - slot_gap))
    else:
        return fb


def forge_power(r, delta, gamma, slot_gap, fa, fb):
    if use_pow_test:
        return fb * r
    else:
        b = max(1.0 - f(delta, gamma, slot_gap, fa, fb), 0.0)
        return 1.0 - np.power(b, r)


# Grinding simulation at module level for multiprocessing
def grinding_frequency(arg):
    (bd, r, gamma, slot_gap, fa, fb, nonces) = arg
    if r == 0.0:
        return 0.0

    phi_cache = {}

    # Staking threshold precomputed
    def phi(d):
        if d in phi_cache:
            return phi_cache[d]
        else:
            phi_cache[d] = 1.0 - (1.0 - f(d, gamma, slot_gap, fa, fb)) ** r
            return phi_cache[d]

    branches = np.zeros((1, 2), dtype=int)
    i = 0

    # Maximally extend set of iid nonces with heuristic branching random walk
    # Each generation produces children with increasing block number
    for y in nonces:
        # Accumulate new branches
        new_branches = []
        for branch in branches:
            # If this branch satisfies vrf test for nonce y new child branches are created at the next height
            if y < phi(slots[i] - branch[0]):
                new_branches.append([slots[i], branch[1] + 1])
        for entry in new_branches:
            branches = np.vstack([branches, entry])
        # Remove duplicate branches
        branches = np.unique(branches, axis=0)
        # Among all parent slots, keep the highest generation branch and discard the rest
        slot_set = set()
        for branch in branches:
            slot_set.add(branch[0])
        branch_max = {x: -1 for x in slot_set}
        # Find the maximum generation
        max_block_num = 0
        for slot in slot_set:
            for entry in branches:
                if entry[0] == slot:
                    if entry[1] > branch_max[slot]:
                        branch_max[slot] = entry[1]
                        max_block_num = max(max_block_num, branch_max[slot])
        # Remove all branches below the maximum generation minus the branch depth
        branches = np.array(list(filter(lambda x: max_block_num - x[1] < bd, list(branch_max.items()))))
        i = i + 1
    max_l = 0
    for branch in branches:
        max_l = max(branch[1], max_l)
    return max_l / total_slots


# Parallelized grinding simulation
def mp_grinding_frequency(bd, r_range, gamma, slot_gap, fa, fb, nonces):
    pool = mp.Pool(mp.cpu_count())
    output = pool.map(grinding_frequency, [(bd, r, gamma, slot_gap, fa, fb, nonces) for r in r_range])
    pool.close()
    return output


def line_intersection(l1, l2):
    x_diff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    y_diff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        raise ZeroDivisionError

    d = (det(*l1), det(*l2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return x, y


def find_intersection(curve1, curve2, x_axis):
    i = 0
    if curve1[0] - curve2[0] == 0.0:
        return x_axis[0], 0.0
    sign = (curve1[0] - curve2[0]) / abs(curve1[0] - curve2[0])
    for (c1, c2) in zip(curve1, curve2):
        if sign > 0.0 and c1 - c2 > 0.0 or sign < 0.0 and c1 - c2 < 0.0:
            i = i + 1
        else:
            if i + 1 < len(x_axis):
                return line_intersection(([x_axis[i], curve1[i]], [x_axis[i + 1], curve1[i + 1]]),
                                         ([x_axis[i], curve2[i]], [x_axis[i + 1], curve2[i + 1]]))
            else:
                # return x_axis[len(x_axis)-1], 0.0
                return line_intersection(([x_axis[i - 1], curve1[i - 1]], [x_axis[i], curve1[i]]),
                                         ([x_axis[i - 1], curve2[i - 1]], [x_axis[i], curve2[i]]))


# Numerical routines for calculation of the Probability Density Function (PDF)


def pdf_acc(d, r, gamma, slot_gap, fa, fb, delay, acc):
    if use_pow_test:
        return pdf_acc_pow(d, r, fb, delay, acc)
    else:
        return pdf_acc_pos(d, r, gamma, slot_gap, fa, fb, delay, acc)


def pi_acc(d, r, gamma, slot_gap, fa, fb, delay, acc):
    if use_pow_test:
        return pi_acc_pow(d, r, fb, delay, acc)
    else:
        return pi_acc_pos(d, r, gamma, slot_gap, fa, fb, delay, acc)


def pdf_old(d_axis, r, gamma, slot_gap, fa, fb, delay):
    i = 0
    done = False
    old_value = 0.0
    accumulation = 1.0
    pdf_a = []
    while not done:
        (nd, accumulation) = pdf_acc(i, r, gamma, slot_gap, fa, fb, delay, accumulation)
        if i == max_iter:
            print("Warning: distribution did not converge", nd, accumulation)
        if trunc_error > nd > 0.0 and old_value > 0.0 or accumulation == 0.0 or i == max_iter:
            done = True
        else:
            pdf_a.append(nd)
            old_value = nd
            i = i + 1

    norm = sum(pdf_a)
    pdf_a = np.asarray(pdf_a) / norm
    return np.pad(pdf_a[:len(d_axis)], [(0, max(len(d_axis)-len(pdf_a), 0))], mode='constant')

def pdf(d_axis, r, gamma, slot_gap, fa, fb, delay):
    i = 0
    done = False
    accumulation = 1.0
    pi = []
    pdf_ext = []
    while not done:
        accumulation = pi_acc(i, r, gamma, slot_gap, fa, fb, delay, accumulation)
        if i == max_iter:
            print("Warning: distribution did not converge", accumulation)
        if trunc_error > accumulation >= 0.0 or i == max_iter:
            done = True
        else:
            pi.append(accumulation)
            i = i + 1
    d = -1
    norm = sum(pi)
    if norm == 0.0:
        print("Warning: stationary distribution summed to zero")
    else:
        pi = np.asarray(pi) / norm
    for p in pi:
        d = d + 1
        if d > delay:
            pdf_ext.append(p*forge_power(r, d, gamma, slot_gap, fa, fb))
        else:
            pdf_ext.append(0.0)
    norm2 = sum(pdf_ext)
    pdf_ext = np.asarray(pdf_ext) / norm2
    return np.pad(pdf_ext[:len(d_axis)], [(0, max(len(d_axis)-len(pdf_ext), 0))], mode='constant'), np.pad(pi[:len(d_axis)], [(0, max(len(d_axis)-len(pi), 0))], mode='constant')


def pdf_acc_pos(d, r, gamma, slot_gap, fa, fb, delay, acc):
    if d == 1:
        if d > delay:
            b = max(1.0 - f(d, gamma, slot_gap, fa, fb), 0.0)
            if b == 0.0:
                return 0.0, acc
            else:
                return 1.0 - np.power(b, stake_scale*r), acc
        else:
            return 0.0, acc
    else:
        if d > delay:
            b1 = max(1.0 - f(d - 1, gamma, slot_gap, fa, fb), 0.0)
            b2 = max(1.0 - f(d, gamma, slot_gap, fa, fb), 0.0)
            if b1 == 0.0:
                acc2 = np.power(b1, stake_scale*r) * acc
                return (1.0 - np.power(b2, stake_scale*r)) * acc2, acc2
            else:
                acc2 = np.power(b1, stake_scale*r) * acc
                if b2 == 0.0:
                    return acc, 0.0
                else:
                    return (1.0 - np.power(b2, stake_scale*r)) * acc2, acc2
        else:
            return 0.0, acc


def pdf_acc_pow(d, r, fb, delay, acc):
    if d == 1:
        if d > delay:
            return fb * r, 1.0
        else:
            return 0.0, 1.0
    else:
        if d > delay:
            out2 = (1.0 - fb * r) * acc
            out1 = fb * r * out2
            return out1, out2
        else:
            return 0.0, acc


def pi_acc_pos(d, r, gamma, slot_gap, fa, fb, delay, acc):
    if d == 1:
        return 1.0
    else:
        if d > delay + 1:
            b1 = max(1.0 - f(d - 1, gamma, slot_gap, fa, fb), 0.0)
            return np.power(b1, stake_scale*r) * acc
        else:
            return acc


def pi_acc_pow(d, r, fb, delay, acc):
    if d == 1:
        return 1.0
    else:
        if d > delay + 1:
            return (1.0 - fb * r) * acc
        else:
            return acc

# Block frequency functions


def block_frequency(r, gamma, slot_gap, fa, fb, delay):
    if numerical_method == "trunc":
        return block_frequency_trunc(r, gamma, slot_gap, fa, fb, delay)
    if numerical_method == "pi":
        return block_frequency_pi(r, gamma, slot_gap, fa, fb, delay)
    if numerical_method == "tail":
        return block_frequency_tail(r, gamma, slot_gap, fa, fb, delay)
    if numerical_method == "pi norm":
        return block_frequency_trunc_pi_norm(r, gamma, slot_gap, fa, fb, delay)
    return 0.0


def block_frequency_pi(r, gamma, slot_gap, fa, fb, delay):
    if r > 0.0:
        ns = max(gamma, slot_gap, delay) + 1
        pi = np.empty([ns])
        pbar = np.empty([ns])
        prev = 1.0
        for i in range(ns):
            new = np.power(1.0 - f(i + 1, gamma, slot_gap, fa, fb), r) * prev
            pbar[i] = new
            prev = new

        c1 = 1.0 + sum(pbar[:ns - 3]) + pbar[ns - 2] / (
                1.0 - np.power(1.0 - f(gamma + 1, gamma, slot_gap, fa, fb), r))
        cgp1 = (1.0 - np.power(1.0 - f(gamma + 1, gamma, slot_gap, fa, fb), r)) * (1.0 + sum(pbar[:ns - 2])) + pbar[
            ns - 1]
        for i in range(ns):
            if i == gamma:
                pi[i] = pbar[i] / cgp1
            else:
                pi[i] = pbar[i] / c1
        print(c1, cgp1)
        print(pi, r, gamma, slot_gap, fa, fb, delay)
        if not 0.98 < sum(pi) < 1.02:
            print(sum(pi))
            quit()
        res = 0.0
        for i in range(ns):
            if i == ns - 1:
                res = res  # + pi[i] * (gamma + 1.0 + 1.0/(r*np.log(1-fb)))
            else:
                res = res + (1.0 - np.power(max(1.0 - f(i + 1, gamma, slot_gap, fa, fb), 0.0), r)) * pi[i] * (i + 1)
        return 1.0 / res
    else:
        return 0.0


def block_frequency_tail(r, gamma, slot_gap, fa, fb, delay):
    if r > 0.0:
        block_time = 0.0
        accumulation = 1.0
        ns = int(max(gamma, slot_gap, delay) + 1)
        pdf_a = np.empty([ns])
        for i in range(ns):
            (nd, accumulation) = pdf_acc(i + 1, r, gamma, slot_gap, fa, fb, delay, accumulation)
            pdf_a[i] = nd
        norm = sum(pdf_a)
        pdf_a = pdf_a / norm
        i = 0
        for nd in pdf_a:
            i = i + 1
            if i == ns:
                block_time = block_time + (ns + 1.0 / (r * np.log(1.0 / (1.0 - fb))))
            else:
                block_time = block_time + i * nd

        if block_time > 0.0:
            return 1.0 / block_time
        else:
            return 0.0
    else:
        return 0.0


def block_frequency_trunc(r, gamma, slot_gap, fa, fb, delay):
    res = 0.0
    if r > 0.0:
        i = 0
        done = False
        old_value = 0.0
        accumulation = 1.0
        pdf_a = []
        while not done:
            (nd, accumulation) = pdf_acc(i, r, gamma, slot_gap, fa, fb, delay, accumulation)
            if i == max_iter:
                print("Warning: distribution did not converge", nd, accumulation)
            if trunc_error > nd > 0.0 and old_value > 0.0 or accumulation == 0.0 or i == max_iter:
                done = True
            else:
                pdf_a.append(nd)
                old_value = nd
                i = i + 1
        d = 0
        norm = sum(pdf_a)
        if norm == 0.0:
            print("Warning: distribution summed to zero")
        else:
            pdf_a = np.asarray(pdf_a) / norm
        for nd in pdf_a:
            d = d + 1
            res = res + d * nd
        if res > 0.0:
            return 1.0 / res
        else:
            return 0.0
    else:
        return 0.0


def block_frequency_trunc_pi_norm(r, gamma, slot_gap, fa, fb, delay):
    res = 0.0
    if r > 0.0:
        i = 0
        done = False
        accumulation = 1.0
        pi = []
        pdf_ext = []
        while not done:
            accumulation = pi_acc(i, r, gamma, slot_gap, fa, fb, delay, accumulation)
            if i == max_iter:
                print("Warning: distribution did not converge", accumulation)
            if trunc_error > accumulation >= 0.0 or i == max_iter:
                done = True
            else:
                pi.append(accumulation)
                i = i + 1
        d = -1
        norm = sum(pi)
        if norm == 0.0:
            print("Warning: stationary distribution summed to zero")
        else:
            pi = np.asarray(pi) / norm
        for p in pi:
            d = d + 1
            if d > delay:
                pdf_ext.append(p*forge_power(r, d, gamma, slot_gap, fa, fb))
            else:
                pdf_ext.append(0.0)
        norm2 = sum(pdf_ext)
        if norm2 == 0.0:
            print("Warning: stationary distribution summed to zero")
        else:
            pdf_ext = np.asarray(pdf_ext) / norm2
        d = -1
        for nd in pdf_ext:
            d = d + 1
            res = res + d * nd
        if res > 0.0:
            return 1.0 / res
        else:
            return 0.0
    else:
        return 0.0


def new_nonces():
    return np.random.rand(total_slots)


if __name__ == '__main__':

    # Plots

    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(15.5, 6.5)
    plt.subplots_adjust(left=0.15, bottom=0.45, wspace=0.25)
    init_density, init_pi = pdf(delta_axis, init_stake, gamma_init, slot_gap_init, fa_init, fb_init, delay_init)
    line0, = ax[0].plot(delta_axis, init_density, label="PDF of Honest Extensions")
    line00, = ax[0].plot(delta_axis, init_pi, label="Stationary Distribution")
    line000, = ax[0].plot(delta_axis, [f(i, gamma_init, slot_gap_init, fa_init, fb_init) for i in delta_axis], 'g:', label="Difficulty Curve")
    # ax[0].set_ylim([0, max(np.amax(init_density), np.amax(init_pi))])
    ax[0].set(xlabel="Slot Interval $\delta$")
    ax[0].set(ylabel="Probability Density")

    h_init_data = [block_frequency(r, gamma_init, slot_gap_init, fa_init, fb_init, delay_init) for r in r_axis]
    a_init_data = [block_frequency(1.0 - r, gamma_init, slot_gap_init, fa_init, fb_init, 0) for r in r_axis]
    line1, = ax[1].plot(r_axis, h_init_data, 'b-', label='honest (r)')
    line2, = ax[1].plot(r_axis, a_init_data, 'r-', label='covert (1-r)')
    line3, = ax[1].plot([0.0, 1.0], [0.0, max(h_init_data)], 'g-', label='$f_{\mathrm{effective}} \cdot r$')
    line4, = ax[1].plot(r_axis, a_init_data, color='r', linestyle='dotted', label='grind (1-r)')

    (inter_x, inter_y) = find_intersection(a_init_data, h_init_data, r_axis)

    dot, = ax[1].plot(inter_x, inter_y, 'ro')

    ax[1].set(xlabel="Active Stake (r)")
    ax[1].set(ylabel="Block Frequency (1/slot)")

    ax[2].set(xlabel="Adversarial Stake")
    ax[2].set(ylabel="$\log_{10}(P_{\mathrm{Settlement Violation}})$ at $k = "+str(k_settle)+"$ blocks")
    prob_settlement = settlement_argument(a_init_data, h_init_data)
    line5, = ax[2].plot(np.flip(r_axis), prob_settlement)
    line6, = ax[2].plot([1.0 - inter_x, 1.0 - inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)], "r--")
    fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - inter_x))

    lim_1 = 0.15
    lim_2 = np.linspace(0.01, 0.31, 7)
    lim_3 = 0.65
    lim_4 = 0.035

    ax_gamma = plt.axes([lim_1, lim_2[0], lim_3, lim_4])
    s_gamma = Slider(ax_gamma, '$\gamma$', 0, gamma_max, valinit=gamma_init, valfmt="%i")

    ax_slot_gap = plt.axes([lim_1, lim_2[1], lim_3, lim_4])
    s_slot_gap = Slider(ax_slot_gap, '$\psi$', 0, gamma_max, valinit=slot_gap_init, valfmt="%i")

    ax_delay = plt.axes([lim_1, lim_2[2], lim_3, lim_4])
    s_delay = Slider(ax_delay, '$\Delta$', 0, gamma_max, valinit=delay_init, valfmt="%i")

    ax_fa = plt.axes([lim_1, lim_2[3], lim_3, lim_4])
    s_fa = Slider(ax_fa, '$f_A$', 0.0, 1.0, valinit=fa_init)

    ax_fb = plt.axes([lim_1, lim_2[4], lim_3, lim_4])
    s_fb = Slider(ax_fb, '$f_B$', 0.001, 0.99, valinit=fb_init)

    ax_grind_button = plt.axes([lim_1, lim_2[5], lim_3, lim_4])
    b_grind = Button(ax_grind_button, 'Calculate Grinding Frequency')

    ax_consistency_plotter = plt.axes([lim_1, lim_2[6], lim_3, lim_4])
    b_plot_consist = Button(ax_consistency_plotter, 'Plot Consistency Heatmap')

    ax[1].legend()
    line4.set_linestyle("None")

    fig2 = plt.figure(2)
    ax2 = plt.axes(projection='3d')
    rax = plt.axes([0.05, 0.95, 0.9, 0.05])
    radio = MyRadioButtons(rax, ['fa', 'fb', 'gamma', 'slot gap', 'delay'], active=4, activecolor='crimson',
                           orientation="horizontal")

    xx = np.linspace(0.0, 1.0, nx)
    yy = np.linspace(0.0, 1.0, ny)
    yyi = np.arange(0, gamma_max, gamma_max / ny)

    zv = np.empty([nx, ny])
    zv2 = np.empty([nx, ny])
    pb3d = np.empty([3, ny])
    zv.fill(0.0)
    zv2.fill(0.0)
    pb3d.fill(0.0)
    xv, yv = np.meshgrid(xx, yy)
    _, yvi = np.meshgrid(xx, yyi)

    surf1 = ax2.plot_surface(xv, yv, zv, zorder=0.3)
    surf2 = ax2.plot_surface(xv, yv, zv, zorder=0.2)
    scatter = ax2.scatter(pb3d[0, :], pb3d[1, :], pb3d[2, :], color='black', marker='x', zorder=0.1)

    ax2.set_xlabel('r')
    ax2.set_zlabel('Block Frequency')
    radio_var = 'delay'

    fig3, ax3 = plt.subplots()
    f_effective = np.amax(zv2)
    curve_consistency, = ax3.plot(pb3d[1, :] * f_effective, 1.0 - pb3d[0, :], label="PoS", color='g')
    block_per_delay = np.linspace(0.0, np.amax(pb3d[1, :] * f_effective), len(pb3d[1, :]))
    pow_consistency_bound = v_pow_bound(block_per_delay)
    curve_pow, = ax3.plot(block_per_delay, pow_consistency_bound, label="PoW", color='b', linestyle=':')

    ax3.set(xlabel="Blocks per Delay Interval $(f_{effective} * \Delta)$")
    ax3.set(ylabel="Consistency Bound")
    ax3.legend()


    def plot_data_points():
        def multi_dict(k, v):
            if k == 1:
                return defaultdict(v)
            else:
                return defaultdict(lambda: multi_dict(k - 1, v))
        hist_data = multi_dict(1, int)
        data = np.loadtxt(dataFileName, dtype=int)
        data_unique = np.unique(data, axis=0)
        dat = data_unique[np.argsort(data_unique[:,0])]
        i = 1
        for row in dat:
            if i < len(dat):
                if row[0] != dat[i][0]-1:
                    print("error: "+str(i))
                else:
                    delta = dat[i][1]-row[1]
                    hist_data[delta] += 1
                i += 1
        hist = hist_data
        deltas = []
        values = []
        for key in hist:
            deltas.append(key)
            values.append(hist[key])
        norm = sum(values)
        def normalize(number):
            return float(number)/norm
        norm_values = [normalize(number) for number in values]
        ax[0].scatter(deltas, norm_values, color="g", marker="x", label="Data from Network")


    def plot_consistency_heatmap(val):
        gamma_axis = np.arange(1, gamma_max + 1)
        fa_axis = np.linspace(0.0, 1.0, 100)
        num_delta = gamma_max
        fig4, ax4 = plt.subplots()
        y_c, x_c = np.meshgrid(gamma_axis, fa_axis)
        z_c = np.empty([len(gamma_axis), len(fa_axis)])
        for (i, val_i) in zip(range(len(gamma_axis)), gamma_axis):
            for (j, val_j) in zip(range(len(fa_axis)), fa_axis):
                z_c[j, i] = np.log(block_frequency(1.0, val_i, s_slot_gap.val, val_j, s_fb.val, 0))
        ax4.contour(x_c, y_c, z_c, levels=40)
        ax4.set(xlabel="$f_A$")
        ax4.set(ylabel="$\gamma$")
        plt.show(block=False)

        y_hm, x_hm = np.meshgrid(gamma_axis, np.linspace(0.0, 100 * target_f_eff, num_delta))
        z_hm = v_pow_bound(x_hm)
        z_hm = z_hm[:-1, :-1]
        fa = 0.0
        f_eff = 0.0
        f_eff_jm1 = 0.0
        for i in range(gamma_max - 1):
            for (j, val) in zip(range(len(fa_axis)), fa_axis):
                f_eff_j = block_frequency(1.0, gamma_axis[i], s_slot_gap.val, val, s_fb.val, 0)
                if f_eff_j > target_f_eff:
                    x1 = fa_axis[j]
                    x2 = fa_axis[j - 1]
                    z11 = f_eff_j
                    z12 = f_eff_jm1
                    z21 = target_f_eff
                    z22 = target_f_eff
                    (fa, f_eff) = line_intersection(([x1, z11], [x2, z12]), ([x1, z21], [x2, z22]))
                    break
                else:
                    f_eff_jm1 = f_eff_jm1
            print("gamma", gamma_axis[i], "fa", fa, "f_eff", f_eff)
            s_gamma.set_val(gamma_axis[i])
            s_fa.set_val(fa)
            adv_data = np.empty(len(r_axis))
            adv_r_axis = [1.0 - r for r in r_axis]
            if heatmap_grind:
                adv_data = mp_grinding_frequency(branch_depth, adv_r_axis, gamma_axis[i], s_slot_gap.val, fa, s_fb.val, ys)
            else:
                for (j, val) in zip(range(len(r_axis)), r_axis):
                    adv_data[j] = block_frequency(1.0 - val, gamma_axis[i], s_slot_gap.val, fa, s_fb.val, 0.0)
            cb = update_cont(radio_var, np.asarray(adv_data), False)
            for (j, val) in zip(range(len(cb) - 1), cb):
                z_hm[j, i] = val - z_hm[j, i]
        z_min, z_max = -np.abs(z_hm).max(), np.abs(z_hm).max()
        fig5, ax5 = plt.subplots()
        c = ax5.pcolormesh(x_hm, y_hm, z_hm, cmap='RdBu', vmin=z_min, vmax=z_max)
        ax5.set_title('Relative Consistency Bound with $f_{effective}$ = ' + str(target_f_eff))
        ax5.axis([x_hm.min(), x_hm.max(), y_hm.min(), y_hm.max()])
        ax5.set(xlabel="Blocks per Delay Interval $(f_{effective} * \Delta)$")
        ax5.set(ylabel="Gamma (Forging Window Cutoff)")
        fig5.colorbar(c, ax=ax5)
        plt.show(block=False)


    def update_consistency(adv_data=np.asarray([]), show=True):
        max_iter_cons = 10
        global curve_consistency, curve_pow, block_per_delay, pow_consistency_bound, f_effective
        if show:
            curve_pow.remove()
            curve_consistency.remove()
        scale_factor = 2
        f_effective = np.amax(zv2)
        block_per_delay = np.linspace(0.0, np.amax(pb3d[1, :]) * f_effective * scale_factor, n_cons_plt)
        pow_consistency_bound = v_pow_bound(block_per_delay)
        consistency_bound = v_pow_bound(block_per_delay)
        window = 0.005
        w0 = 0.005
        c0 = 0.5
        if len(adv_data) == 0:
            for d in np.array(range(0, scale_factor * n_cons_plt, scale_factor)):
                i = 0
                while i < max_iter_cons:
                    try:
                        x1 = c0 - window
                        x2 = c0 + window
                        z11 = block_frequency(x1, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, d)
                        z12 = block_frequency(x2, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, d)
                        z21 = block_frequency(1.0 - x1, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0)
                        z22 = block_frequency(1.0 - x2, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0)
                        (xi, zi) = line_intersection(([x1, z11], [x2, z12]), ([x1, z21], [x2, z22]))
                        consistency_bound[d // scale_factor] = 1.0 - xi
                        c0 = xi
                        i = max_iter_cons
                    except ZeroDivisionError:
                        window = window + w0
                        i = i + 1
                        # print("increasing window")
        else:
            interp = interpolate.interp1d(r_axis, adv_data, kind="cubic")
            c0, z0 = find_intersection(zv[0, :], interp(xv[0, :]), xv[0, :])
            for d in np.array(range(0, scale_factor * n_cons_plt, scale_factor)):
                i = 0
                while i < max_iter_cons:
                    try:
                        x1 = c0 - window
                        x2 = c0 + window
                        z11 = block_frequency(x1, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, d)
                        z12 = block_frequency(x2, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, d)
                        z21 = interp(x1)
                        z22 = interp(x2)
                        (xi, zi) = line_intersection(([x1, z11], [x2, z12]), ([x1, z21], [x2, z22]))
                        consistency_bound[d // scale_factor] = 1.0 - xi
                        c0 = xi
                        i = max_iter_cons
                    except ZeroDivisionError:
                        window = window + w0
                        i = i + 1
                        # print("increasing window")
        if show:
            curve_consistency, = ax3.plot(block_per_delay, consistency_bound, label="PoS", color='g')
            curve_pow, = ax3.plot(block_per_delay, pow_consistency_bound, label="PoW", color='b', linestyle=':')
            ax3.relim()
            ax3.autoscale_view()
        return consistency_bound


    def update_cont(label, adv_data=np.asarray([]), show=True):
        global surf1, surf2, scatter, radio_var
        ch = 'winter'
        ca = 'autumn'
        if show:
            surf1.remove()
            surf2.remove()
        radio_var = label
        if radio_var == 'gamma':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], yvi[j, i], s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val)
                    zv2[j, i] = block_frequency(1.0 - xv[j, i], yvi[j, i], s_slot_gap.val, s_fa.val, s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yvi[j, 0]
                pb3d[2, j] = pbz
            if show:
                surf1 = ax2.plot_surface(xv, yvi, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
                surf2 = ax2.plot_surface(xv, yvi, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
                scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'slot gap':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, yvi[j, i], s_fa.val, s_fb.val, s_delay.val)
                    zv2[j, i] = block_frequency(1.0 - xv[j, i], s_gamma.val, yvi[j, i], s_fa.val, s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yvi[j, 0]
                pb3d[2, j] = pbz
            if show:
                surf1 = ax2.plot_surface(xv, yvi, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
                surf2 = ax2.plot_surface(xv, yvi, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
                scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'fa':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, s_slot_gap.val, yv[j, i], s_fb.val, s_delay.val)
                    zv2[j, i] = block_frequency(1.0 - xv[j, i], s_gamma.val, s_slot_gap.val, yv[j, i], s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yv[j, 0]
                pb3d[2, j] = pbz
            if show:
                surf1 = ax2.plot_surface(xv, yv, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
                surf2 = ax2.plot_surface(xv, yv, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
                scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'fb':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, yv[j, i], s_delay.val)
                    zv2[j, i] = block_frequency(1.0 - xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, yv[j, i], 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yv[j, 0]
                pb3d[2, j] = pbz
            surf1 = ax2.plot_surface(xv, yv, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
            surf2 = ax2.plot_surface(xv, yv, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
            scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'delay':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, yvi[j, i])
                    zv2[j, i] = block_frequency(1.0 - xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yvi[j, 0]
                pb3d[2, j] = pbz
            if show:
                surf1 = ax2.plot_surface(xv, yvi, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
                surf2 = ax2.plot_surface(xv, yvi, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
                scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if show:
            ax2.set_ylabel(label)
            ax2.relim()
            ax2.autoscale_view(tight=True)
            ax2.set_zlim3d(0.0, min(1.0, max(np.amax(zv), np.amax(zv2))))
        cb = update_consistency(adv_data, show)
        if show:
            plt.show(block=False)
        return cb


    def update_gamma(new_gamma):
        new_data = [block_frequency(r, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for r in
                    r_axis]
        new_data2 = [block_frequency(1.0 - r, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
        new_density, new_pi = pdf(delta_axis, 1.0, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val)
        line0.set_ydata(new_density)
        line00.set_ydata(new_pi)
        line000.set_ydata([f(i, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val) for i in delta_axis])
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        global prob_settlement
        prob_settlement = settlement_argument(new_data2, new_data)
        line5.set_ydata(prob_settlement)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        line6.set_data([1.0 - new_inter_x, 1.0 - new_inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].set_ylim([0, max(np.amax(new_density), np.amax(new_pi))])
        ax[1].relim()
        ax[1].autoscale_view()
        ax[2].relim()
        ax[2].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_slot_gap(new_slot_gap):
        new_data = [block_frequency(r, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, s_delay.val) for r in
                    r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, 0) for r in r_axis]
        new_density, new_pi = pdf(delta_axis, 1.0, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, s_delay.val)
        line0.set_ydata(new_density)
        line00.set_ydata(new_pi)
        line000.set_ydata([f(i, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val) for i in delta_axis])
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        global prob_settlement
        prob_settlement = settlement_argument(new_data2, new_data)
        line5.set_ydata(prob_settlement)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        line6.set_data([1.0 - new_inter_x, 1.0 - new_inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].set_ylim([0, max(np.amax(new_density), np.amax(new_pi))])
        ax[1].relim()
        ax[1].autoscale_view()
        ax[2].relim()
        ax[2].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_fa(new_fa):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, s_delay.val) for r in r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, 0) for r in r_axis]
        new_density, new_pi = pdf(delta_axis, 1.0, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, s_delay.val)
        line0.set_ydata(new_density)
        line00.set_ydata(new_pi)
        line000.set_ydata([f(i, s_gamma.val,  s_slot_gap.val, new_fa, s_fb.val) for i in delta_axis])
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        global prob_settlement
        prob_settlement = settlement_argument(new_data2, new_data)
        line5.set_ydata(prob_settlement)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        line6.set_data([1.0 - new_inter_x, 1.0 - new_inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].set_ylim([0, max(np.amax(new_density), np.amax(new_pi))])
        ax[1].relim()
        ax[1].autoscale_view()
        ax[2].relim()
        ax[2].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_fb(new_fb):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, s_delay.val) for r in r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, 0) for r in r_axis]
        new_density, new_pi = pdf(delta_axis, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, s_delay.val)
        line0.set_ydata(new_density)
        line00.set_ydata(new_pi)
        line000.set_ydata([f(i, s_gamma.val,  s_slot_gap.val, s_fa.val, new_fb) for i in delta_axis])
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        global prob_settlement
        prob_settlement = settlement_argument(new_data2, new_data)
        line5.set_ydata(prob_settlement)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        line6.set_data([1.0 - new_inter_x, 1.0 - new_inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].set_ylim([0, max(np.amax(new_density), np.amax(new_pi))])
        ax[1].relim()
        ax[1].autoscale_view()
        ax[2].relim()
        ax[2].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_delay(new_delay):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, round(new_delay)) for r in
                    r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
        new_density, new_pi = pdf(delta_axis, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, round(new_delay))
        line0.set_ydata(new_density)
        line00.set_ydata(new_pi)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        global prob_settlement
        prob_settlement = settlement_argument(new_data2, new_data)
        line5.set_ydata(prob_settlement)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        line6.set_data([1.0 - new_inter_x, 1.0 - new_inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].set_ylim([0, max(np.amax(new_density), np.amax(new_pi))])
        ax[1].relim()
        ax[1].autoscale_view()
        ax[2].relim()
        ax[2].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_grind(val):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for r in r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
        adv_r_axis = [1.0-r for r in r_axis]
        new_data3 = mp_grinding_frequency(branch_depth, adv_r_axis, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, ys)
        new_density, new_pi = pdf(delta_axis, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val)
        line0.set_ydata(new_density)
        line00.set_ydata(new_pi)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data3)
        line4.set_linestyle('dotted')
        global prob_settlement
        prob_settlement = settlement_argument(new_data2, new_data)
        line5.set_ydata(prob_settlement)
        (new_inter_x, new_inter_y) = find_intersection(new_data3, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        line6.set_data([1.0 - new_inter_x, 1.0 - new_inter_x], [np.nanmin(prob_settlement), np.nanmax(prob_settlement)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].set_ylim([0, max(np.amax(new_density), np.amax(new_pi))])
        ax[1].relim()
        ax[1].autoscale_view()
        ax[2].relim()
        ax[2].autoscale_view()
        update_cont(radio_var)
        update_consistency(np.asarray(new_data3))
        fig.suptitle("Consistency Bound = " + "{:.2f}".format(1.0 - new_inter_x))

    if plot_data:
        plot_data_points()
    ax[0].legend()
    update_cont(radio_var)
    s_gamma.on_changed(update_gamma)
    s_slot_gap.on_changed(update_slot_gap)
    s_fa.on_changed(update_fa)
    s_fb.on_changed(update_fb)
    s_delay.on_changed(update_delay)
    b_grind.on_clicked(update_grind)
    b_plot_consist.on_clicked(plot_consistency_heatmap)
    # radio.on_clicked(update_cont)


plt.show()
