from relative_forging_power import *

if __name__ == '__main__':

    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })

    # Grinding advantage plots
    fig = plt.figure()
    fig.set_size_inches(w=4.7747, h=3.5)
    axx = fig.add_subplot(1, 1, 1)
    axx.plot(r_axis, [block_frequency(r, 15, slot_gap_init, fa_init, fb_init, 0) for r in r_axis], label="$\omega$", color="green")

    print("working on 1")
    axx.scatter(r_axis, mp_grinding_frequency(16, r_axis, 15, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=16)$", marker="o", color="red")
    print("working on 2")
    axx.scatter(r_axis, mp_grinding_frequency(4, r_axis, 15, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=4)$", marker="x", color="orange")
    print("working on 3")
    axx.scatter(r_axis, mp_grinding_frequency(2, r_axis, 15, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=2)$", marker="+", color="yellow")
    print("working on 4")
    axx.scatter(r_axis, mp_grinding_frequency(1, r_axis, 15, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=1)$", marker=".", color="blue")
    axx.legend()
    axx.set_xlabel("$r$")
    axx.set_ylabel("Frequency (1/slot)")
    handles, labels = axx.get_legend_handles_labels()
    axx.legend(handles[::-1], labels[::-1])
    matplotlib.pyplot.savefig('grind_d_2_4_16_g_15.pgf')

    fig = plt.figure()
    fig.set_size_inches(w=4.7747, h=3.5)
    axx = fig.add_subplot(1, 1, 1)
    axx.plot(r_axis, [block_frequency(r, 40, slot_gap_init, fa_init, fb_init, 0) for r in r_axis], label="$\omega$", color="green")

    print("working on 5")
    axx.scatter(r_axis, mp_grinding_frequency(16, r_axis, 40, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=16)$", marker="o", color="red")
    print("working on 6")
    axx.scatter(r_axis, mp_grinding_frequency(4, r_axis, 40, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=4)$", marker="x", color="orange")
    print("working on 7")
    axx.scatter(r_axis, mp_grinding_frequency(2, r_axis, 40, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=2)$", marker="+", color="yellow")
    print("working on 8")
    axx.scatter(r_axis, mp_grinding_frequency(1, r_axis, 40, slot_gap_init, fa_init, fb_init), label="$\omega_g (d=1)$", marker=".", color="blue")
    axx.legend()
    axx.set_xlabel("$r$")
    axx.set_ylabel("Frequency (1/slot)")
    handles, labels = axx.get_legend_handles_labels()
    axx.legend(handles[::-1], labels[::-1])
    matplotlib.pyplot.savefig('grind_d_2_4_16_g_40.pgf')
