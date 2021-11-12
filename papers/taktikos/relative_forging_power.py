import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

trunc_error = 1.0e-5


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
        return [np.power(1.0 - f(k), r) for k in range(1, j+1)]

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
        if x < slot_gap + 1:
            return 0.0
        elif x < gamma + 1:
            return fa * (float(x - slot_gap)) / float(gamma - slot_gap)
        else:
            return fb

    def prod_p_empty_slot(j):
        return np.power(1.0 - f(j), r)*acc

    if d < delay+1:
        return 0.0, 1.0
    elif d < 1:
        return 0.0, 1.0
    elif d == 1:
        return 1.0 - np.power(1.0 - f(d), r), 1.0
    else:
        out2 = prod_p_empty_slot(d - 1)
        out1 = (1.0 - np.power(1.0 - f(d), r)) * out2
        return out1, out2


def block_frequency(r, gamma, slot_gap, fa, fb, delay):
    res = 0.0
    if r > 0.0:
        i = 0
        done = False
        old_value = 0.0
        accumulation = 0.0
        while not done:
            i = i + 1
            (nd, accumulation) = n_d_acc(i, r, gamma, slot_gap, fa, fb, delay, accumulation)
            new = i * nd
            if new < trunc_error and old_value > 0.0:
                done = True
            res = res + new
            old_value = new
        if res > 0.0:
            return 1.0/res
        else:
            return 0.0
    else:
        return 0.0


gamma_init = 0
fa_init = 0.5
fb_init = 0.05
slot_gap_init = 0
delay_init = 0

delta_axis = range(0, 101)
r_axis = np.linspace(0.0, 1.0, 20)

fig, ax = plt.subplots(1, 2)
plt.subplots_adjust(left=0.15, bottom=0.4)
init_density = [n_d(d, 1.0, gamma_init, slot_gap_init, fa_init, fb_init, delay_init) for d in delta_axis]
line0, = ax[0].plot(delta_axis, init_density)
ax[0].set(xlabel="Slot Interval")
ax[0].set(ylabel="Probability Density")

r_init_data = [block_frequency(r, gamma_init, slot_gap_init, fa_init, fb_init, delay_init) for r in r_axis]
a_init_data = [block_frequency(1.0-r, gamma_init, slot_gap_init, fa_init, fb_init, 0) for r in r_axis]
line1, = ax[1].plot(r_axis, r_init_data, 'b-')
line2, = ax[1].plot(r_axis, a_init_data, 'r-')
line3, = ax[1].plot([0.0, 1.0], [0.0, max(r_init_data)], 'g-')


def line_intersection(l1, l2):
    x_diff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    y_diff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*l1), det(*l2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return x, y


def find_intersection(curve1, curve2, x_axis):
    i = 0
    sign = (curve1[0]-curve2[0])/abs(curve1[0]-curve2[0])
    for (c1, c2) in zip(curve1, curve2):
        if sign > 0.0 and c1-c2 > 0.0 or sign < 0.0 and c1-c2 < 0.0:
            i = i+1
        else:
            return line_intersection(([x_axis[i], curve1[i]], [x_axis[i+1], curve1[i+1]]), ([x_axis[i], curve2[i]], [x_axis[i+1], curve2[i+1]]))


(inter_x, inter_y) = find_intersection(a_init_data, r_init_data, r_axis)

dot, = ax[1].plot(inter_x, inter_y, 'ro')

ax[1].set(xlabel="Active Stake (r)")
ax[1].set(ylabel="Block Frequency (1/slot)")
fig.suptitle("Participation Bound = "+"{:.2f}".format(1.0-inter_x))

ax_gamma = plt.axes([0.15, 0.05, 0.65, 0.03])
s_gamma = Slider(ax_gamma, 'gamma', 0, 100, valinit=gamma_init, valfmt="%i")

ax_slot_gap = plt.axes([0.15, 0.1, 0.65, 0.03])
s_slot_gap = Slider(ax_slot_gap, 'slot gap', 0, 100, valinit=slot_gap_init, valfmt="%i")

ax_delay = plt.axes([0.15, 0.15, 0.65, 0.03])
s_delay = Slider(ax_delay, 'delay', 0, 100, valinit=delay_init, valfmt="%i")

ax_fa = plt.axes([0.15, 0.2, 0.65, 0.03])
s_fa = Slider(ax_fa, 'fA', 0.001, 0.99, valinit=fa_init)

ax_fb = plt.axes([0.15, 0.25, 0.65, 0.03])
s_fb = Slider(ax_fb, 'fB', 0.001, 0.99, valinit=fb_init)


def update_gamma(new_gamma):
    new_data = [block_frequency(r, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for r in r_axis]
    new_data2 = [block_frequency(1.0-r, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
    new_density = [n_d(d, 1.0, round(new_gamma), s_slot_gap.val, s_fa.val, s_fb.val, s_delay.val) for d in delta_axis]
    line0.set_ydata(new_density)
    line1.set_ydata(new_data)
    line2.set_ydata(new_data2)
    line3.set_ydata([0.0, max(new_data)])
    (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
    dot.set_xdata(new_inter_x)
    dot.set_ydata(new_inter_y)
    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    fig.suptitle("Participation Bound = "+"{:.2f}".format(1.0-new_inter_x))


def update_slot_gap(new_slot_gap):
    new_data = [block_frequency(r, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, s_delay.val) for r in r_axis]
    new_data2 = [block_frequency(1.0-r, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, 0) for r in r_axis]
    new_density = [n_d(d, 1.0, s_gamma.val, round(new_slot_gap), s_fa.val, s_fb.val, s_delay.val) for d in delta_axis]
    line0.set_ydata(new_density)
    line1.set_ydata(new_data)
    line2.set_ydata(new_data2)
    line3.set_ydata([0.0, max(new_data)])
    (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
    dot.set_xdata(new_inter_x)
    dot.set_ydata(new_inter_y)
    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    fig.suptitle("Participation Bound = "+"{:.2f}".format(1.0-new_inter_x))


def update_fa(new_fa):
    new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, s_delay.val) for r in r_axis]
    new_data2 = [block_frequency(1.0-r, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, 0) for r in r_axis]
    new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, new_fa, s_fb.val, s_delay.val) for d in delta_axis]
    line0.set_ydata(new_density)
    line1.set_ydata(new_data)
    line2.set_ydata(new_data2)
    line3.set_ydata([0.0, max(new_data)])
    (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
    dot.set_xdata(new_inter_x)
    dot.set_ydata(new_inter_y)
    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    fig.suptitle("Participation Bound = "+"{:.2f}".format(1.0-new_inter_x))


def update_fb(new_fb):
    new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, s_delay.val) for r in r_axis]
    new_data2 = [block_frequency(1.0-r, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, 0) for r in r_axis]
    new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, new_fb, s_delay.val) for d in delta_axis]
    line0.set_ydata(new_density)
    line1.set_ydata(new_data)
    line2.set_ydata(new_data2)
    line3.set_ydata([0.0, max(new_data)])
    (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
    dot.set_xdata(new_inter_x)
    dot.set_ydata(new_inter_y)
    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    fig.suptitle("Participation Bound = "+"{:.2f}".format(1.0-new_inter_x))


def update_delay(new_delay):
    new_data = [block_frequency(r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, round(new_delay)) for r in r_axis]
    new_data2 = [block_frequency(1.0-r, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, 0) for r in r_axis]
    new_density = [n_d(d, 1.0, s_gamma.val, s_slot_gap.val, s_fa.val, s_fb.val, round(new_delay)) for d in delta_axis]
    line0.set_ydata(new_density)
    line1.set_ydata(new_data)
    line2.set_ydata(new_data2)
    line3.set_ydata([0.0, max(new_data)])
    (new_inter_x, new_inter_y) = find_intersection(new_data2, new_data, r_axis)
    dot.set_xdata(new_inter_x)
    dot.set_ydata(new_inter_y)
    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    fig.suptitle("Participation Bound = "+"{:.2f}".format(1.0-new_inter_x))


s_gamma.on_changed(update_gamma)
s_slot_gap.on_changed(update_slot_gap)
s_fa.on_changed(update_fa)
s_fb.on_changed(update_fb)
s_delay.on_changed(update_delay)


plt.show()


