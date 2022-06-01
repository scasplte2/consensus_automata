import random

import numpy as np
import matplotlib.pyplot as plt


# Set seed for reproducibility
seed = 1
np.random.seed(seed)

# Number of Slots
total_slots = 300000
# Slots
slots = np.arange(total_slots)
# Forging window
gamma = 40
# Slot gap
slot_gap = 0
# Snowplow amplitude
fa = 0.4
# Baseline difficulty
fb = 0.05
# Maximum difference between leading block number and viable branches
# branches with a gap greater than branchDepth are cut
branchDepth = 2

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
        if self.ys[slot] < self.threshold(slot-parentSlot):
            return True
        else:
            return False


# Selects branch to serve to challengers
def select_branch(branches):
    bn = 0
    ps = total_slots + 1
    for branch in branches:
        bn = max(bn, branch[1])
    for branch in branches:
        if bn == branch[1]:
            ps = min(ps, branch[0])
    return [ps, bn]


# Simulation with heuristic branching random walk
# Each generation produces children with increasing block number
def grinding_sim(num_challenger, num_adversary):

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

    # Main for loop over all slots
    for slot in slots:

        # Accumulate new branches
        new_branches = []

        # Adaptively corrupt random challengers
        random.shuffle(challengers)
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
        for entry in new_branches:
            branches = np.vstack([branches, entry])
        # Remove duplicate branches
        branches = np.unique(branches, axis=0)
        # Among all parent slots, keep the highest generation branch and discard the rest
        slot_set = set()
        for branch in branches:
            slot_set.add(branch[0])
        branch_max = {x: -1 for x in slot_set}
        branch_reserve = {x: -1 for x in slot_set}
        # Find the maximum generation
        max_block_num = 0
        for sl in slot_set:
            for entry in branches:
                if entry[0] == sl:
                    if entry[1] > branch_max[sl]:
                        branch_max[sl] = entry[1]
                        branch_reserve[sl] = entry[2]
                        max_block_num = max(max_block_num, branch_max[sl])

        def add_reserve(b):
            return np.concatenate((np.asarray(b), [branch_reserve[b[0]]]), axis=0)

        # Remove all branches below the maximum generation minus the branch depth
        branches = np.array(list(
            map(add_reserve, list(filter(lambda x: max_block_num - x[1] < branchDepth, list(branch_max.items()))))
        ))
        leading_honest_block = 0
        reach = 0

        def add_margin(b):
            gap = leading_honest_block - (b[1]-b[2])
            reserve = b[2]
            return [b[0], b[1], b[2], reserve - gap]

        for branch in branches:
            leading_honest_block = max(branch[1]-branch[2], leading_honest_block)
        for branch in branches:
            if branch[1]-branch[2] == leading_honest_block:
                reach = max(branch[2], reach)
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
            forks = forks + 1
        else:
            if forked:
                forked = False
                j = j+1
                avg_settle = avg_settle * (j-1)/j + (leading_honest_block - last_fork)/j
    max_l = 0
    num_b = 0
    for branch in branches:
        max_l = max(branch[1], max_l)
        num_b = num_b + 1
    hud = ("Average Margin: "+str(avg_margin)) \
        + ("\nFork length: " + str(avg_settle)) \
        + ("\nFork rate: " + str(forks/total_slots)) \
        + ("\nMaximum block number: " + str(max_l)) \
        + ("\nFinal number of branches: " + str(num_b)) \
        + "\n[Parent slot, block number, reserve, margin]:\n" + str(branches)
    print(hud)
    return [max_l, avg_settle, forks/total_slots, avg_margin]


avg_data = []
frk_data = []
mrg_data = []
adv_axis = []

data_points = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99]

for k in data_points:
    print(k)
    data = grinding_sim(100, k)
    avg_data.append(data[1])
    frk_data.append(data[2])
    mrg_data.append(data[3])
    adv_axis.append(k/100)
plt.figure()
plt.plot(adv_axis, frk_data)
plt.xlabel("Adversary fraction")
plt.ylabel("Proportion of time in a forked state")
plt.figure()
plt.plot(adv_axis, avg_data)
plt.xlabel("Adversary fraction")
plt.ylabel("Average settlement depth (blocks)")
plt.figure()
plt.plot(adv_axis, mrg_data)
plt.xlabel("Adversary fraction")
plt.ylabel("Average margin")
plt.show()
