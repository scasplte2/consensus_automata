from relative_forging_power import *


# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
#     'axes.unicode_minus': False
# })

def grinding_frequency(delay, gamma, slot_gap, fa, fb):
    bd = 1
    r = 1.0
    nonces = new_nonces()
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
            if y < phi(slots[i] - branch[0]) and slots[i] - branch[0] > delay:
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


data_points = range(20)


def trend1_freq(delay):
    return block_frequency(1, 15, 0, 0.5, 0.05, delay)


trend1 = list(map(trend1_freq, data_points))


def trend2_freq(delay):
    return block_frequency(1, 0, 0, 0.5, 0.05, delay)


trend2 = list(map(trend2_freq, data_points))
plt.figure()
plt.plot(data_points, trend1, label="Taktikos")
plt.plot(data_points, trend2, label="Praos")
plt.xlabel("$\Delta$")
plt.ylabel("$\omega$")
plt.legend()
plt.title("Honest chain growth vs. delay")
plt.tight_layout()
# matplotlib.pyplot.savefig('frequency_vs_delay.pgf')

plt.figure()

init_density, init_pi = pdf(delta_axis, init_stake, gamma_init, slot_gap_init, fa_init, fb_init, 0)
init_density_2, init_pi_2 = pdf(delta_axis, init_stake, 0, slot_gap_init, fa_init, 0.05, 0)
plt.plot(delta_axis, init_density)
plt.plot(delta_axis, init_density_2)
plt.show()
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
print(i)
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
print(i)
