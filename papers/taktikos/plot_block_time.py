from relative_forging_power import *


matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'axes.unicode_minus': False
})


def grinding_frequency(delay, gamma, slot_gap, fa, fb, hist_data, max_slot):
    bd = 1
    r = 1.0
    nonces = np.random.rand(max_slot)
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
            delta = i - branch[0]
            if y < phi(delta) and delta > delay:
                new_branches.append([i, branch[1] + 1])
                if delta in hist_data.keys():
                    hist_data.update({delta: hist_data.get(delta) + 1})
                else:
                    hist_data.update({delta: 1})
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
    return max_l / max_slot


maximum_slot = 100000
data_points = range(20)
num_trials = 30


def trend1_freq(delay):
    return block_frequency(1, 15, 0, 0.5, 0.05, delay)


def trend2_freq(delay):
    return block_frequency(1, 0, 0, 0.5, 0.05, delay)


def trend3_freq(delay):
    print(delay)
    return grinding_frequency(delay, 15, 0, 0.5, 0.05, {}, maximum_slot)


def trend4_freq(delay):
    print(delay)
    return grinding_frequency(delay, 0, 0, 0.5, 0.05, {}, maximum_slot)


trend1 = list(map(trend1_freq, data_points))
trend2 = list(map(trend2_freq, data_points))

print("working on 1")
data_set_1 = []
for i in range(num_trials):
    print("trial "+str(i))
    data_set_1.append(list(map(trend3_freq, data_points)))
trend_1 = np.array(data_set_1).mean(axis=0, dtype=np.float64)
error_1 = np.array(data_set_1).std(axis=0, dtype=np.float64)

print("working on 2")
data_set_2 = []
for i in range(num_trials):
    print("trial "+str(i))
    data_set_2.append(list(map(trend4_freq, data_points)))
trend_2 = np.array(data_set_2).mean(axis=0, dtype=np.float64)
error_2 = np.array(data_set_2).std(axis=0, dtype=np.float64)

plt.figure()
plt.plot(data_points, trend1, label="Predicted (Taktikos)", color="blue")
plt.scatter(data_points, trend_1, label="Experiment (Taktikos)", marker="o", color="blue")
plt.errorbar(data_points, trend_1, yerr=error_1, fmt="o", color="blue")
plt.plot(data_points, trend2, label="Predicted (Praos)", color="orange")
plt.scatter(data_points, trend_2, label="Experiment (Praos)", marker="o", color="orange")
plt.errorbar(data_points, trend_2, yerr=error_2, fmt="o", color="orange")
plt.xlabel("$\Delta$")
plt.ylabel("$\omega$")
plt.legend()
handles, labels = plt.gca().get_legend_handles_labels()
order = [0, 2, 1, 3]
plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
# plt.title("Honest chain growth vs. delay")
plt.xticks(np.arange(min(data_points), max(data_points)+1, 2.0))
plt.ylim([0.0, 0.16])
plt.tight_layout()
matplotlib.pyplot.savefig('frequency_vs_delay.pgf')


plt.figure()

init_density, init_pi = pdf(delta_axis, init_stake, 15, 0, 0.5, 0.05, 0)
histogram_data = {}
histogram_data_2 = {}
output = grinding_frequency(0, 15, 0, 0.5, 0.05, histogram_data, maximum_slot*10)
output2 = grinding_frequency(0, 0, 0, 0.5, 0.05, histogram_data_2, maximum_slot*10)
init_density_2, init_pi_2 = pdf(delta_axis, init_stake, 0, slot_gap_init, fa_init, 0.05, 0)
sum = 0.0
for key in histogram_data.keys():
    sum = sum + histogram_data.get(key)
values = []
for key in histogram_data.keys():
    values.append(histogram_data.get(key)/sum)
sum = 0.0
for key in histogram_data_2.keys():
    sum = sum + histogram_data_2.get(key)
values2 = []
for key in histogram_data_2.keys():
    values2.append(histogram_data_2.get(key)/sum)

print("Expectation of block time for Taktikos:")
mu1 = np.sum(delta_axis * init_density)
vector1 = (delta_axis - mu1)**2
var1 = np.sum(init_density * vector1)
print(mu1)
print(var1)
sum = 0.0
i = 0
for value in init_density:
    if sum < 0.99:
        sum = sum + value
        i = i + 1
percentile1 = i
print("Expectation of block time for Praos:")
mu2 = np.sum(delta_axis * init_density_2)
vector2 = (delta_axis - mu2)**2
var2 = np.sum(init_density_2 * vector2)
print(mu2)
print(var2)
sum = 0.0
i = 0
for value in init_density_2:
    if sum < 0.99:
        sum = sum + value
        i = i + 1
percentile2 = i

plt.plot(delta_axis[1:], init_density[1:], label="Predicted (Taktikos)", color="blue")
plt.scatter(histogram_data.keys(), values, label="Experiment (Taktikos)", color="blue")
plt.plot([mu1, mu1], [0.0, 1.0], linestyle='dotted', color="blue", label="Expectation (Taktikos)")
plt.plot([percentile1, percentile1], [0.0, 1.0], linestyle='dashdot', color="blue", label="$99^{\mathrm{th}}$ Percentile (Taktikos)")
plt.plot(delta_axis[1:], init_density_2[1:], label="Predicted (Praos)", color="orange")
plt.scatter(histogram_data_2.keys(), values2, label="Experiment (Praos)", color="orange")
plt.plot([mu2, mu2], [0.0, 1.0], linestyle='dotted', color="orange", label="Expectation (Praos)")
plt.plot([percentile2, percentile2], [0.0, 1.0], linestyle='dashdot', color="orange", label="$99^{\mathrm{th}}$ Percentile (Praos)")

plt.legend()
handles, labels = plt.gca().get_legend_handles_labels()
order = [0, 1, 2, 6, 3, 4, 5, 7]
plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
plt.xlabel("Block time interval $\delta$")
plt.ylabel("Probability")
plt.xlim([0, 100])
plt.ylim([0.0, 0.14])

plt.tight_layout()
matplotlib.pyplot.savefig('Block_time_interval.pgf')

# plt.show()


