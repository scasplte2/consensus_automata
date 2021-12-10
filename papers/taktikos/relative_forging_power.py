import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.widgets import Button
import multiprocessing as mp
from mpl_toolkits import mplot3d
from matplotlib.widgets import AxesWidget, RadioButtons

gamma_max = 100
trunc_error = 1.0e-4
max_iter = 3000
total_slots = 100000
slots = np.arange(total_slots)
ys = np.random.rand(total_slots)
branch_depth = 2
nx, ny = (10, 10)
gamma_init = 0
fa_init = 0.5
fb_init = 0.05
slot_gap_init = 0
delay_init = 0


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
            p = ax.scatter([],[], s=size, marker="o", edgecolor='black',
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
        self.cnt = 0
        self.observers = {}

        self.connect_event('pick_event', self._clicked)

    def _clicked(self, event):
        if (self.ignore(event) or event.mouseevent.button != 1 or
                event.mouseevent.inaxes != self.ax):
            return
        if event.artist in self.circles:
            self.set_active(self.circles.index(event.artist))


def grinding_frequency(arg):
    (bd, r, gamma, slot_gap, fa, fb) = arg
    if r == 0.0:
        return 0.0

    # Snowplow curve
    def f(x):
        if x < slot_gap + 1:
            return 0.0
        elif x < gamma + 1:
            return fa * (float(x - slot_gap)) / float(gamma - slot_gap)
        else:
            return fb

    phi_cache = {}

    # Staking threshold
    def phi(d):
        if d in phi_cache:
            return phi_cache[d]
        else:
            phi_cache[d] = 1.0 - (1.0 - f(d)) ** r
            return phi_cache[d]

    branches = np.zeros((1, 2), dtype=int)
    i = 0

    for y in ys:
        new_parents = []
        for branch in branches:
            if y < phi(slots[i] - branch[0]):
                new_parents.append([branch[0], branch[1]])
                branch[0] = slots[i]
                branch[1] = branch[1] + 1
        for entry in new_parents:
            branches = np.vstack([branches, entry])
        branches = np.unique(branches, axis=0)
        slot_set = set()
        for branch in branches:
            slot_set.add(branch[0])
        branch_max = {x: -1 for x in slot_set}
        max_block_num = 0
        for slot in slot_set:
            for entry in branches:
                if entry[0] == slot:
                    if entry[1] > branch_max[slot]:
                        branch_max[slot] = entry[1]
                        max_block_num = max(max_block_num, branch_max[slot])
        branches = np.array(list(filter(lambda x: max_block_num - x[1] < bd, list(branch_max.items()))))
        i = i + 1
    max_l = 0
    for branch in branches:
        max_l = max(branch[1], max_l)
    return max_l / total_slots


def mp_grinding_frequency(r_range, gamma, slot_gap, fa, fb):
    pool = mp.Pool(mp.cpu_count())
    output = pool.map(grinding_frequency, [(branch_depth, 1.0 - arg, gamma, slot_gap, fa, fb) for arg in r_range])
    pool.close()
    return output


if __name__ == '__main__':

    def n_d(d, r, gamma, slot_gap, fa, fb, delay):
        def f(x):
            if x < slot_gap + 1:
                return 0.0
            elif x < gamma + 1:
                return fa * (float(x - slot_gap)) / float(gamma - slot_gap)
            else:
                return fb

        def prod(arguments):
            result = 1.0
            for k in arguments:
                result = result * k
            return result

        def p_empty_slot(j):
            return [np.power(1.0 - f(k), r) for k in range(1, j + 1)]

        def prod_p_empty_slot(j):
            return prod(p_empty_slot(j))

        if d < 1 or d < delay + 1:
            return 0.0
        elif d == 1:
            return 1.0 - np.power(1.0 - f(d), r)
        else:
            return (1.0 - np.power(1.0 - f(d), r)) * prod_p_empty_slot(d - 1)


    def n_d_acc(d, r, gamma, slot_gap, fa, fb, delay, acc):
        def f(x):
            if x <= slot_gap or x <= delay:
                return 0.0
            elif x <= gamma:
                return fa * (float(x - slot_gap)) / float(gamma - slot_gap)
            else:
                return fb
        if d == 1:
            return 1.0 - np.power(max(1.0 - f(d), 0.0), r), 1.0
        else:
            out2 = np.power(max(1.0 - f(d-1), 0.0), r) * acc
            out1 = (1.0 - np.power(max(1.0 - f(d), 0.0), r)) * out2
            return out1, out2

    def n_d_acc_pow(d, r, gamma, slot_gap, fa, fb, delay, acc):
        def f(x, y):
            if y <= delay:
                return 0.0
            else:
                return fb*x
        if d == 1:
            return f(r, d), 1.0
        else:
            out2 = (1.0 - f(r, d)) * acc
            out1 = f(r, d) * out2
            return out1, out2

    def block_frequency_pi(r, gamma, slot_gap, fa, fb, delay):
        if r > 0.0:
            def f(x):
                if x < slot_gap + 1 or x < delay + 1:
                    return 0.0
                elif x < gamma + 1:
                    return fa * (float(x - slot_gap)) / float(gamma - slot_gap)
                else:
                    return fb
            ns = max(gamma, slot_gap, delay) + 1
            pi = np.empty([ns])
            pbar = np.empty([ns])
            prev = 1.0
            for i in range(ns):
                new = np.power(1.0 - f(i+1), r) * prev
                pbar[i] = new
                prev = new

            c1 = 1.0 + sum(pbar[:ns-3]) + pbar[ns-2]/(1.0 - np.power(1.0 - f(gamma+1), r))
            cgp1 = (1.0 - np.power(1.0 - f(gamma+1), r)) * (1.0 + sum(pbar[:ns-2])) + pbar[ns-1]
            for i in range(ns):
                if i == gamma:
                    pi[i] = pbar[i]/cgp1
                else:
                    pi[i] = pbar[i]/c1
            print(c1, cgp1)
            print(pi, r, gamma, slot_gap, fa, fb, delay)
            if not 0.98 < sum(pi) < 1.02:
                print(sum(pi))
                quit()
            res = 0.0
            for i in range(ns):
                if i == ns-1:
                    res = res  # + pi[i] * (gamma + 1.0 + 1.0/(r*np.log(1-fb)))
                else:
                    res = res + (1.0 - np.power(max(1.0 - f(i+1), 0.0), r)) * pi[i] * (i + 1)
            return 1.0 / res
        else:
            return 0.0


    def block_frequency_tail(r, gamma, slot_gap, fa, fb, delay):
        if r > 0.0:
            block_time = 0.0
            accumulation = 0.0
            ns = int(max(gamma, slot_gap, delay) + 1)
            pdf = np.empty([ns])
            for i in range(ns):
                (nd, accumulation) = n_d_acc(i+1, r, gamma, slot_gap, fa, fb, delay, accumulation)
                pdf[i] = nd
            norm = sum(pdf)
            pdf = pdf/norm
            i = 0
            for nd in pdf:
                i = i + 1
                if i == ns:
                    block_time = block_time + (ns + 1.0/(r*np.log(1.0/(1.0 - fb))))
                else:
                    block_time = block_time + i * nd

            if block_time > 0.0:
                return 1.0 / block_time
            else:
                return 0.0
        else:
            return 0.0


    def block_frequency(r, gamma, slot_gap, fa, fb, delay):
        res = 0.0
        if r > 0.0:
            i = 0
            done = False
            old_value = 0.0
            accumulation = 0.0
            pdf = []
            while not done and i < max_iter:
                i = i + 1
                (nd, accumulation) = n_d_acc(i, r, gamma, slot_gap, fa, fb, delay, accumulation)
                # new = i * nd
                pdf.append(nd)
                new = nd
                if trunc_error > new > 0.0 and old_value > 0.0:
                    done = True
                old_value = new
            i = 0
            for nd in pdf:
                i = i + 1
                res = res + i * nd
            if res > 0.0:
                return 1.0 / res
            else:
                return 0.0
        else:
            return 0.0

    delta_axis = range(0, gamma_max+1)
    r_axis = np.linspace(0.0, 1.0, 20)

    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(left=0.15, bottom=0.4)
    init_density = [n_d(d, 1.0, gamma_init, slot_gap_init, fa_init, fb_init, delay_init) for d in delta_axis]
    line0, = ax[0].plot(delta_axis, init_density)
    ax[0].set(xlabel="Slot Interval")
    ax[0].set(ylabel="Probability Density")

    r_init_data = [block_frequency(r, gamma_init, slot_gap_init, fa_init, fb_init, delay_init) for r in r_axis]
    a_init_data = [block_frequency(1.0 - r, gamma_init, slot_gap_init, fa_init, fb_init, 0) for r in r_axis]
    line1, = ax[1].plot(r_axis, r_init_data, 'b-', label='honest (r)')
    line2, = ax[1].plot(r_axis, a_init_data, 'r-', label='covert (1-r)')
    line3, = ax[1].plot([0.0, 1.0], [0.0, max(r_init_data)], 'g-', label='f_eff * r')
    line4, = ax[1].plot(r_axis, a_init_data, color='r', linestyle='dotted', label='grind (1-r)')


    def line_intersection(l1, l2):
        x_diff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
        y_diff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(x_diff, y_diff)
        if div == 0:
            return 0.0, 0.0
            # raise Exception('lines do not intersect')

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
                if i+1 < len(x_axis):
                    return line_intersection(([x_axis[i], curve1[i]], [x_axis[i + 1], curve1[i + 1]]),
                                             ([x_axis[i], curve2[i]], [x_axis[i + 1], curve2[i + 1]]))
                else:
                    return x_axis[len(x_axis)-1], 0.0


    (inter_x, inter_y) = find_intersection(a_init_data, r_init_data, r_axis)

    dot, = ax[1].plot(inter_x, inter_y, 'ro')

    ax[1].set(xlabel="Active Stake (r)")
    ax[1].set(ylabel="Block Frequency (1/slot)")
    fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - inter_x))

    ax_gamma = plt.axes([0.15, 0.05, 0.65, 0.03])
    s_gamma = Slider(ax_gamma, 'gamma', 0, gamma_max, valinit=gamma_init, valfmt="%i")

    ax_slot_gap = plt.axes([0.15, 0.1, 0.65, 0.03])
    s_slot_gap = Slider(ax_slot_gap, 'slot gap', 0, gamma_max, valinit=slot_gap_init, valfmt="%i")

    ax_delay = plt.axes([0.15, 0.15, 0.65, 0.03])
    s_delay = Slider(ax_delay, 'delay', 0, gamma_max, valinit=delay_init, valfmt="%i")

    ax_fa = plt.axes([0.15, 0.2, 0.65, 0.03])
    s_fa = Slider(ax_fa, 'fA', 0.001, 0.99, valinit=fa_init)

    ax_fb = plt.axes([0.15, 0.25, 0.65, 0.03])
    s_fb = Slider(ax_fb, 'fB', 0.001, 0.99, valinit=fb_init)

    ax_grind_button = plt.axes([0.15, 0.01, 0.65, 0.03])
    b_grind = Button(ax_grind_button, 'Calculate Grinding Advantage')

    ax[1].legend()
    line4.set_linestyle("None")

    fig2 = plt.figure(2)
    ax2 = plt.axes(projection='3d')
    rax = plt.axes([0.05, 0.95, 0.9, 0.05])
    radio = MyRadioButtons(rax, ['fa', 'fb', 'gamma', 'slot gap', 'delay'], active=4, activecolor='crimson',
                           orientation="horizontal")

    xx = np.linspace(0.0, 1.0, nx)
    yy = np.linspace(0.0, 1.0, ny)
    yyi = np.arange(0, gamma_max, gamma_max/ny)

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

    def update_cont(label):
        global surf1, surf2, scatter, radio_var
        ch = 'winter'
        ca = 'autumn'
        surf1.remove()
        surf2.remove()
        radio_var = label
        if radio_var == 'gamma':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], yvi[j, i], s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val)
                    zv2[j, i] = block_frequency(1.0-xv[j, i], yvi[j, i], s_slot_gap.val, s_fa.val, s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yvi[j, 0]
                pb3d[2, j] = pbz
            surf1 = ax2.plot_surface(xv, yvi, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
            surf2 = ax2.plot_surface(xv, yvi, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
            scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'slot gap':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, yvi[j, i], s_fa.val, s_fb.val, s_delay.val)
                    zv2[j, i] = block_frequency(1.0-xv[j, i], s_gamma.val, yvi[j, i], s_fa.val, s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yvi[j, 0]
                pb3d[2, j] = pbz
            surf1 = ax2.plot_surface(xv, yvi, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
            surf2 = ax2.plot_surface(xv, yvi, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
            scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'fa':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, s_slot_gap.val, yv[j, i], s_fb.val, s_delay.val)
                    zv2[j, i] = block_frequency(1.0-xv[j, i], s_gamma.val, s_slot_gap.val, yv[j, i], s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yv[j, 0]
                pb3d[2, j] = pbz
            surf1 = ax2.plot_surface(xv, yv, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
            surf2 = ax2.plot_surface(xv, yv, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
            scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        if radio_var == 'fb':
            for i in range(nx):
                for j in range(ny):
                    zv[j, i] = block_frequency(xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, yv[j, i], s_delay.val)
                    zv2[j, i] = block_frequency(1.0-xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, yv[j, i], 0)
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
                    zv2[j, i] = block_frequency(1.0-xv[j, i], s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0)
            for j in range(ny):
                pbx, pbz = find_intersection(zv[j, :], zv2[j, :], xv[j, :])
                pb3d[0, j] = pbx
                pb3d[1, j] = yvi[j, 0]
                pb3d[2, j] = pbz
            surf1 = ax2.plot_surface(xv, yvi, zv, linewidth=0, antialiased=True, cmap=ch, alpha=0.5)
            surf2 = ax2.plot_surface(xv, yvi, zv2, linewidth=0, antialiased=True, cmap=ca, alpha=0.5)
            scatter._offsets3d = (pb3d[0, :], pb3d[1, :], pb3d[2, :])
        ax2.set_ylabel(label)
        ax2.relim()
        ax2.autoscale_view(tight=True)
        ax2.set_zlim3d(0.0, min(1.0, max(np.amax(zv), np.amax(zv2))))
        plt.show(block=False)


    def update_gamma(new_gamma):
        new_data = [block_frequency(r, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for r in
                    r_axis]
        new_data2 = [block_frequency(1.0 - r, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
        new_density = [n_d(d, 1.0, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for d in
                       delta_axis]
        line0.set_ydata(new_density)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_slot_gap(new_slot_gap):
        new_data = [block_frequency(r, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, s_delay.val) for r in
                    r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, 0) for r in r_axis]
        new_density = [n_d(d, 1.0, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, s_delay.val) for d in
                       delta_axis]
        line0.set_ydata(new_density)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_fa(new_fa):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, s_delay.val) for r in r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, 0) for r in r_axis]
        new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, s_delay.val) for d in delta_axis]
        line0.set_ydata(new_density)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_fb(new_fb):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, s_delay.val) for r in r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, 0) for r in r_axis]
        new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, s_delay.val) for d in delta_axis]
        line0.set_ydata(new_density)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_delay(new_delay):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, round(new_delay)) for r in
                    r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
        new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, round(new_delay)) for d in
                       delta_axis]
        line0.set_ydata(new_density)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data2)
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    def update_grind(val):
        new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for r in r_axis]
        new_data2 = [block_frequency(1.0 - r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
        new_data3 = mp_grinding_frequency(r_axis, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val)
        new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for d in delta_axis]
        line0.set_ydata(new_density)
        line1.set_ydata(new_data)
        line2.set_ydata(new_data2)
        line3.set_ydata([0.0, max(new_data)])
        line4.set_ydata(new_data3)
        line4.set_linestyle('dotted')
        (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
        dot.set_xdata(new_inter_x)
        dot.set_ydata(new_inter_y)
        ax[0].relim()
        ax[0].autoscale_view()
        ax[1].relim()
        ax[1].autoscale_view()
        update_cont(radio_var)
        fig.suptitle("Participation Bound = " + "{:.2f}".format(1.0 - new_inter_x))


    update_cont(radio_var)
    s_gamma.on_changed(update_gamma)
    s_slot_gap.on_changed(update_slot_gap)
    s_fa.on_changed(update_fa)
    s_fb.on_changed(update_fb)
    s_delay.on_changed(update_delay)
    b_grind.on_clicked(update_grind)
    radio.on_clicked(update_cont)

    fig3 = plt.figure(3)
    ax3 = plt.axes()
    scale_factor = np.amax(zv2)
    ax3.plot(pb3d[1, :]*scale_factor, 1.0-pb3d[0, :], label="PoS")
    x_axis = np.linspace(0.001, np.amax(pb3d[1, :]*scale_factor), len(pb3d[1, :]))
    y_data = 0.5 + (2.0 - np.sqrt(x_axis*x_axis + 4.0))/(2.0*x_axis)
    ax3.plot(x_axis, y_data, label="PoW")
    ax3.plot()

    ax3.set(xlabel="Chain Growth * Delay (f_eff * Delta)")
    ax3.set(ylabel="Consistency Bound")
    ax3.legend()


plt.show()
