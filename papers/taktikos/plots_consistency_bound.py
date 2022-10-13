from relative_forging_power import *

if __name__ == '__main__':
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        'axes.unicode_minus': False
    })

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
    fig3.set_size_inches(w=4.7747, h=3.5)
    f_effective = np.amax(zv2)
    curve_consistency, = ax3.plot(pb3d[1, :] * f_effective, 1.0 - pb3d[0, :], label="Taktikos", color='g')
    curve_praos, = ax3.plot(pb3d[1, :] * f_effective, 1.0 - pb3d[0, :], label="Praos", color='r')
    block_per_delay = np.linspace(0.0, np.amax(pb3d[1, :] * f_effective), len(pb3d[1, :]))
    pow_consistency_bound = v_pow_bound(block_per_delay)
    curve_pow, = ax3.plot(block_per_delay, pow_consistency_bound, label="PoW", color='b', linestyle=':')

    ax3.set(xlabel="Blocks per Delay Interval")
    ax3.set(ylabel="Consistency Bound")
    ax3.legend()
    ax3.set_xlim(0.0, 5.0)

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


    def update_consistency_praos(adv_data=np.asarray([]), show=True):
        max_iter_cons = 10
        global curve_praos
        if show:
            curve_praos.remove()
        scale_factor = 2
        f_effective = block_frequency(1.0, 0, 0, 0, s_fb.val, 0)
        block_per_delay = np.linspace(0.0, np.amax(pb3d[1, :]) * f_effective * scale_factor, n_cons_plt)
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
                        z11 = block_frequency(x1, 0, 0, 0, s_fb.val, d)
                        z12 = block_frequency(x2, 0, 0, 0, s_fb.val, d)
                        z21 = block_frequency(1.0 - x1, 0, 0, 0, s_fb.val, 0)
                        z22 = block_frequency(1.0 - x2, 0, 0, 0, s_fb.val, 0)
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
                        z11 = block_frequency(x1, 0, 0, 0, s_fb.val, d)
                        z12 = block_frequency(x2, 0, 0, 0, s_fb.val, d)
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
            curve_praos, = ax3.plot(block_per_delay, consistency_bound, label="Praos", color='r')
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
        update_consistency_praos(adv_data, show)
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
    plt.tight_layout()
    matplotlib.pyplot.savefig('consistency_bound_plots.pgf')
    # radio.on_clicked(update_cont)

