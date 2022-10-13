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

    fig = plt.figure()
    fig.set_size_inches(w=4.7747, h=3.5)
    axx = fig.add_subplot(1, 1, 1)
    h_init_data_1 = [block_frequency(1.0-r, gamma_init, slot_gap_init, fa_init, fb_init, 0) for r in r_axis]
    h_init_data_2 = [block_frequency(1.0-r, gamma_init, slot_gap_init, fa_init, fb_init, 5) for r in r_axis]
    h_init_data_3 = [block_frequency(1.0-r, gamma_init, slot_gap_init, fa_init, fb_init, 10) for r in r_axis]
    h_init_data_4 = [block_frequency(1.0-r, gamma_init, slot_gap_init, fa_init, fb_init, 20) for r in r_axis]
    a_init_data = [block_frequency(r, gamma_init, slot_gap_init, fa_init, fb_init, 0) for r in r_axis]
    axx.plot(r_axis, a_init_data, label="$\omega_\mathcal{A}$", color="red")
    axx.plot(r_axis, h_init_data_1, label="$\omega_\mathcal{H}, \Delta = 0$", color="blue")
    axx.plot(r_axis, h_init_data_2, label="$\omega_\mathcal{H}, \Delta = 5$", color="green")
    axx.plot(r_axis, h_init_data_3, label="$\omega_\mathcal{H}, \Delta = 10$", color="orange")
    axx.plot(r_axis, h_init_data_4, label="$\omega_\mathcal{H}, \Delta = 20$", color="magenta")
    (inter_x, inter_y) = find_intersection(a_init_data, h_init_data_1, r_axis)
    axx.plot(inter_x, inter_y, 'bo')
    (inter_x, inter_y) = find_intersection(a_init_data, h_init_data_2, r_axis)
    axx.plot(inter_x, inter_y, 'go')
    (inter_x, inter_y) = find_intersection(a_init_data, h_init_data_3, r_axis)
    axx.plot(inter_x, inter_y, 'o', color="orange")
    (inter_x, inter_y) = find_intersection(a_init_data, h_init_data_4, r_axis)
    axx.plot(inter_x, inter_y, 'o', color="magenta")
    axx.set_xlabel("Adversary Fraction")
    axx.set_ylabel("Block Frequency (1/slot)")
    axx.legend()
    plt.tight_layout()
    matplotlib.pyplot.savefig('relative_plots.pgf')

