
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import matplotlib

# Set seed for reproducibility
seed = 1
np.random.seed(seed)

# Number of Slots
total_slots = 10000
# Slots
slots = np.arange(total_slots)
# Forging window
gamma = 15
# Slot gap
slot_gap = 0
# Snowplow amplitude
fa = 0.5
# Baseline difficulty
fb = 0.05


k_settle = 10


# Use a specified difficulty curve from txt
user_defined_curve = False

# User defined curve TODO add txt file input
l = 10
# difficulty_curve = np.sqrt(delta_axis)*0.01
# difficulty_curve = delta_axis*delta_axis*0.0005
# difficulty_curve = (signal.sawtooth(2 * np.pi * 0.1 * delta_axis) + 1.0) / 2.0
difficulty_curve = np.mod(np.arange(0, gamma + 1), l)/float(l-1)


# Difficulty curve
def f(delta):
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


# Staking threshold
def phi(d, a):
    return 1.0 - (1.0 - f(d)) ** a


def generate_nonces():
    return np.random.rand(total_slots)


class Challenger:

    def __init__(self, stake):
        self.stake = stake
        self.ys = generate_nonces()
        self.phi_cache = {}
        self.block_number = 0
        self.parent_slot = 0
        self.reserve = 0

    # Staking threshold precomputed
    def threshold(self, d):
        if d in self.phi_cache:
            return self.phi_cache[d]
        else:
            self.phi_cache[d] = phi(d, self.stake)
            return self.phi_cache[d]

    def test(self, slot, parentSlot):
        if self.ys[slot % total_slots] < self.threshold(slot-parentSlot):
            return True
        else:
            return False


# Selects branch to serve to challengers
def select_branch(branches):
    branches = branches[branches[:, 1].argsort()]
    # print(branches)
    bn = 0
    ps = 100000000000000
    for branch in branches:
        bn = max(bn, branch[1] - branch[2])
    for branch in branches:
        if bn == branch[1] - branch[2]:
            ps = min(ps, branch[0])

    return [ps, bn]


# Simulation with heuristic branching random walk
# Each generation produces children with increasing block number
def grinding_sim(arg):
    (num_challenger, num_adversary) = arg
    # Maximum difference between leading block number and viable branches
    # branches with a gap greater than branchDepth are cut
    branch_depth = 2
    # Set of challengers with equal resources
    challengers = [Challenger(1.0/num_challenger) for i in range(num_challenger)]

    branches = np.zeros((1, 4), dtype=int)

    # Variables for tracking forks
    forks = 0
    avg_settle = 0.0
    avg_margin = 0.0
    forked = False
    last_fork = 0
    j = 0
    jj = 0
    fork_intervals = []
    # Main for loop over all slots
    # for slot in slots:
    slot = 0
    reach = 0
    margin = 0
    while len(fork_intervals) < 10000:
    # while slot < total_slots:
        # Accumulate new branches
        new_branches = []

        # Adaptively corrupt random challengers
        np.random.shuffle(challengers)
        honest = challengers[num_adversary:]
        adversary = challengers[:num_adversary]

        # Selects the branch that the honest challengers extend
        honest_branch = select_branch(branches)
        for challenger in honest:
            # If this branch satisfies vrf test new child branches are created at the next height with reserve 0
            if challenger.test(slot, honest_branch[0]):
                new_branches.append([slot, honest_branch[1] + 1, 0, 0])
        for branch in branches:
            for challenger in adversary:
                # If this branch satisfies vrf test new child branches are created at the next height and next reserve
                if challenger.test(slot, branch[0]):
                    new_branches.append([slot, branch[1] + 1, branch[2] + 1, 0])
        if len(new_branches) > 0:

            for entry in new_branches:
                branches = np.vstack([branches, entry])
            # Remove duplicate branches
            # branches = np.unique(branches, axis=0)
            leading_honest_block = 0

            for branch in branches:
                leading_honest_block = max(branch[1]-branch[2], leading_honest_block)

            def add_margin(b):
                gap = leading_honest_block - (b[1]-b[2])
                reserve = b[2]
                return [b[0], b[1], b[2], reserve - gap]

            branches = np.array(list(map(add_margin, list(branches))))

            num_viable = 0

            for branch in branches:
                jj = jj + 1
                avg_margin = avg_margin * (jj-1)/jj + branch[3] / jj
                if branch[3] >= 0:
                    num_viable = num_viable + 1

            if num_viable >= 2:
                if not forked:
                    forked = True
                    last_fork = leading_honest_block
                elif forked and leading_honest_block - last_fork >= k_settle:
                    forks = forks + 1
                    forked = False
                    j = j+1
                    avg_settle = avg_settle * (j-1)/j + (leading_honest_block - last_fork)/j
                    fork_intervals.append(abs(leading_honest_block - last_fork))
                    branches = np.empty((1, 4), dtype=int)
                    branches = np.vstack([branches, [slot, leading_honest_block, 0, 0]])
            else:
                if forked:
                    forks = forks + 1
                    forked = False
                    j = j+1
                    avg_settle = avg_settle * (j-1)/j + (leading_honest_block - last_fork)/j
                    fork_intervals.append(leading_honest_block - last_fork)
                    branches = np.empty((1, 4), dtype=int)
                    branches = np.vstack([branches, [slot, leading_honest_block, 0, 0]])
                else:
                    fork_intervals.append(0)
            margins = []
            for branch in branches:
                margins.append(branch[3])
            reach = max(margins)
            margins.remove(reach)
            margin = max(margins)

            branches = branches[branches[:, 1].argsort()]
            # if len(new_branches) > 0:
            #     print(branches)
            #     print([reach, margin, slot])
            branches = np.array(list(filter(lambda x: x[3] > -branch_depth, list(branches))))
        if slot % 1000 == 0:
            print([reach, margin, slot, len(branches)])

        slot = slot + 1
    max_l = 0
    num_b = 0
    for branch in branches:
        max_l = max(branch[1], max_l)
        num_b = num_b + 1
    hud = ("Average Margin: "+str(avg_margin)) \
        + ("\nFork length: " + str(avg_settle)) \
        + ("\nFork rate: " + str(forks/slot)) \
        + ("\nMaximum block number: " + str(max_l)) \
        + ("\nFinal number of branches: " + str(num_b)) \
        + "\n[Parent slot, block number, reserve, margin]:\n" + str(branches)
    print(hud)
    return [max_l/slot, avg_settle, forks/slot, avg_margin], fork_intervals


if __name__ == '__main__':
    avg_data = []
    var_data = []
    std_data = []
    frk_data = []
    mrg_data = []
    chg_data = []
    prk_data = []
    adv_axis = []


    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        'axes.unicode_minus': False
    })


    data_points = range(0, 51, 5)

    for k in data_points:
        adv_axis.append(k/100)

    pool = mp.Pool(mp.cpu_count())

    outfile = open('test.npy', 'wb')

    output = pool.map(grinding_sim, [(100, k) for k in data_points])
    for entry in output:
        data, data_forks = entry
        chg_data.append(data[0])
        avg_data.append(np.asarray(data_forks))
        frk_data.append(data[2])
        mrg_data.append(data[3])

    pool.close()

    # plt.figure()
    # plt.plot(adv_axis, frk_data)
    # plt.xlabel("Adversary fraction")
    # plt.ylabel("Proportion of time in a forked state")
    fig = plt.figure()
    fig.set_size_inches(w=4.7747, h=3.5)
    ax = fig.add_subplot(111, projection='3d')
    nbins = 20
    for ys, z in zip(avg_data, adv_axis):
        hist, bins = np.histogram(ys, bins=nbins, density=True, range=(0, nbins))
        xs = (bins[:-1] + bins[1:])/2
        cnt = 0
        for entry in ys:
            if entry >= k_settle:
                cnt = cnt + 1
        prk_data.append(cnt/len(ys))
        ax.bar(xs, hist, zs=z, zdir='y', alpha=0.8)
    ax.axes.set_xlim3d(left=0.0, right=nbins)
    ax.set_xlabel('Fork length')
    ax.set_ylabel('Adversary fraction')
    ax.set_zlabel('Probability Density')
    matplotlib.pyplot.savefig('challenger_hist.pgf')

    fig1 = plt.figure()
    fig1.set_size_inches(w=4.7747, h=3.5)
    ax1 = fig1.add_subplot(111)
    ax1.plot(adv_axis, chg_data)
    ax1.set_xlabel("Adversary fraction")
    ax1.set_ylabel("Effective Growth")
    matplotlib.pyplot.savefig('challenger_growth.pgf')

    fig2 = plt.figure()
    fig2.set_size_inches(w=4.7747, h=3.5)

    ax2 = fig2.add_subplot(111)
    r_axis = np.linspace(0.01, 0.5, 50)
    line = np.power(2*np.asarray(r_axis), k_settle)*np.power(2.0-2*r_axis, k_settle)
    ax2.plot(r_axis, np.log10(line), label="Covert")
    scatter_data_x = []
    scatter_data_y = []
    for r, p in zip(adv_axis, prk_data):
        if p > 0.0:
            scatter_data_x.append(r)
            scatter_data_y.append(np.log10(p))
    ax2.scatter(scatter_data_x, scatter_data_y, label="Grinding", color="red", marker=".")
    ax2.set_xlabel("Adversary fraction")
    ax2.set_ylabel("Log Pr[settlement violation] for $k = "+str(k_settle)+"$")
    ax2.legend()
    matplotlib.pyplot.savefig('challenger_settle.pgf')

    # hits = []
    #
    # for ys, z in zip(avg_data, adv_axis):
    #     plt.figure()
    #     hits.append(len(ys))
    #     plt.hist(ys)
    #     plt.title("Adversary Fraction: "+str(z))
    #     plt.xlabel("Fork length")
    #     plt.ylabel("Number of forks")
    #     plt.show()
    #
    # plt.figure()
    # plt.plot(adv_axis, hits)
    # plt.xlabel("Adversary fraction")
    # plt.ylabel("Number of forks")
    # plt.show()
    #

