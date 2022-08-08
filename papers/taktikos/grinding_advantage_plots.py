from relative_forging_power import *

if __name__ == '__main__':

    import csv

    num_trials = 30

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
    data_set_1 = []
    for i in range(num_trials):
        print(i)
        data_set_1.append(mp_grinding_frequency(16, r_axis, 15, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_1 = np.array(data_set_1).mean(axis=0, dtype=np.float64)
    error_1 = np.array(data_set_1).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_1, label="$\omega_g (d=16)$", marker="o", color="red")
    axx.errorbar(r_axis, trend_1, yerr=error_1, fmt="o", color="red")

    print("working on 2")
    data_set_2 = []
    for i in range(num_trials):
        print(i)
        data_set_2.append(mp_grinding_frequency(4, r_axis, 15, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_2 = np.array(data_set_2).mean(axis=0, dtype=np.float64)
    error_2 = np.array(data_set_2).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_2, label="$\omega_g (d=4)$", marker="x", color="orange")
    axx.errorbar(r_axis, trend_2, yerr=error_2, fmt="x", color="orange")

    print("working on 3")
    data_set_3 = []
    for i in range(num_trials):
        print(i)
        data_set_3.append(mp_grinding_frequency(2, r_axis, 15, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_3 = np.array(data_set_3).mean(axis=0, dtype=np.float64)
    error_3 = np.array(data_set_3).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_3, label="$\omega_g (d=2)$", marker="+", color="yellow")
    axx.errorbar(r_axis, trend_3, yerr=error_3, fmt="+", color="yellow")

    print("working on 4")
    data_set_4 = []
    for i in range(num_trials):
        print(i)
        data_set_4.append(mp_grinding_frequency(1, r_axis, 15, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_4 = np.array(data_set_4).mean(axis=0, dtype=np.float64)
    error_4 = np.array(data_set_4).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_4, label="$\omega_g (d=1)$", marker=".", color="blue")
    axx.errorbar(r_axis, trend_4, yerr=error_4, fmt=".", color="blue")

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
    data_set_5 = []
    for i in range(num_trials):
        print(i)
        data_set_5.append(mp_grinding_frequency(16, r_axis, 40, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_5 = np.array(data_set_5).mean(axis=0, dtype=np.float64)
    error_5 = np.array(data_set_5).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_5, label="$\omega_g (d=16)$", marker="o", color="red")
    axx.errorbar(r_axis, trend_5, yerr=error_5, fmt="o", color="red")

    print("working on 6")
    data_set_6 = []
    for i in range(num_trials):
        print(i)
        data_set_6.append(mp_grinding_frequency(4, r_axis, 40, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_6 = np.array(data_set_6).mean(axis=0, dtype=np.float64)
    error_6 = np.array(data_set_6).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_6, label="$\omega_g (d=4)$", marker="x", color="orange")
    axx.errorbar(r_axis, trend_6, yerr=error_6, fmt="x", color="orange")

    print("working on 7")
    data_set_7 = []
    for i in range(num_trials):
        print(i)
        data_set_7.append(mp_grinding_frequency(2, r_axis, 40, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_7 = np.array(data_set_7).mean(axis=0, dtype=np.float64)
    error_7 = np.array(data_set_7).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_7, label="$\omega_g (d=2)$", marker="+", color="yellow")
    axx.errorbar(r_axis, trend_7, yerr=error_7, fmt="+", color="yellow")

    print("working on 8")
    data_set_8 = []
    for i in range(num_trials):
        print(i)
        data_set_8.append(mp_grinding_frequency(1, r_axis, 40, slot_gap_init, fa_init, fb_init))
        ys = new_nonces()
    trend_8 = np.array(data_set_8).mean(axis=0, dtype=np.float64)
    error_8 = np.array(data_set_8).std(axis=0, dtype=np.float64)
    axx.scatter(r_axis, trend_8, label="$\omega_g (d=1)$", marker=".", color="blue")
    axx.errorbar(r_axis, trend_8, yerr=error_8, fmt=".", color="blue")

    axx.legend()
    axx.set_xlabel("$r$")
    axx.set_ylabel("Frequency (1/slot)")
    handles, labels = axx.get_legend_handles_labels()
    axx.legend(handles[::-1], labels[::-1])
    matplotlib.pyplot.savefig('grind_d_2_4_16_g_40.pgf')

    with open("data_out_1.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_1)

    with open("data_out_2.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_2)

    with open("data_out_3.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_3)

    with open("data_out_4.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_4)

    with open("data_out_5.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_5)

    with open("data_out_6.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_6)

    with open("data_out_7.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_7)

    with open("data_out_8.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=' ')
        csvWriter.writerows(data_set_8)

