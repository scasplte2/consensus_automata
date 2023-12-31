import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# AMS 2021: Visualization of nothing-at-stake branching with local dynamic difficulty leader eligibility.
# Local difficulty adjustments are shown with tracer colors in the branching diagram (left).
# Adversarial pseudo-predictable nonces are shown in the nonce distribution (right).
# The pseudo-predictable nonces are super-imposed along the diagonal of the branching diagram.
# Vertical solid lines represent extensions, many extensions may overlap with random colors to show complexity.
# Automata are represented as branches (parent slot / block number pairs).
# Honest extensions assume 1-alpha resources split among each maximum length branch with distinct parent slots.

# Set seed for reproducibility
np.random.seed(123)

# Number of Slots
N = 100
# Slots
slots = np.arange(N)
# Adversarial nonces
ys = np.random.rand(N)
# Proportion of adversarial stake
alpha = 0.5
# Forging window
gamma = 40
# Slot gap
slot_gap = 0
# Snowplow amplitude
fa = 0.5
# Baseline difficulty
fb = 0.05
# Maximum difference between leading block number and viable branches
# branches with a gap greater than branchDepth are cut
# branchDepth = 6
# use challenger model, honest extensions
useChallenger = True
# calculate plots
makePlots = True


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


# Nonce distribution plot area and colors
area = []
colors = []


# Generates the spectrum of colors for trails in branching diagram
def genSpectrum(g):
    if g > 0:
        spec = cm.rainbow(np.linspace(0, 1, g))
        spec = np.append(spec, [[0.0, 0.0, 0.0, 1.0]], axis=0)
        return spec
    else:
        return np.array([[1.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 1.0]])


spectrum = genSpectrum(gamma)


def max_block_number(ys,branchDepth):
    if makePlots:
        # Tracer points for nothing-at-stake branching
        trails = np.zeros((N, N), dtype=int)
        fig = plt.figure(figsize=(16, 7))
        subPlotLeft = fig.add_subplot(121)
        subPlotRight = fig.add_subplot(122)
    leadingHonestBlockNumber = 0
    if useChallenger:
        # Empty string with genesis prefix
        # rows are branches, columns are parent slot / block number / reserve
        branches = np.zeros((1, 3), dtype=int)
        honestHeads = np.array([[0, 1.0 - alpha, 0]])
    else:
        # Empty string with genesis prefix
        # rows are branches, columns are parent slot / block number
        branches = np.zeros((1, 2), dtype=int)
    i = 0
    for y in ys:
        if makePlots:
            if gamma > 0:
                if y > phi(gamma, alpha):
                    area.append(1.0)
                    colors.append(spectrum[gamma])
                    subPlotLeft.scatter(slots[i], slots[i], s=1.0, c=spectrum[gamma].reshape(1, -1))
                else:
                    j = gamma
                    while y > phi(gamma - j, alpha):
                        j = j - 1
                    area.append(2.0 * j)
                    colors.append(spectrum[gamma - j])
                    subPlotLeft.scatter(slots[i], slots[i], s=j, c=spectrum[gamma - j].reshape(1, -1), alpha=0.5)
            else:
                if y > phi(1, alpha):
                    area.append(1.0)
                    colors.append(spectrum[1])
                    subPlotLeft.scatter(slots[i], slots[i], s=1.0, c=spectrum[1].reshape(1, -1))
                else:
                    area.append(25.0)
                    colors.append(spectrum[0])
                    subPlotLeft.scatter(slots[i], slots[i], s=25.0, c=spectrum[0].reshape(1, -1), alpha=0.5)
        newParents = []
        for branch in branches:
            oldParent = branch[0]
            if y < phi(slots[i] - branch[0], alpha):
                if useChallenger:
                    newParents.append([branch[0], branch[1], branch[2]])
                else:
                    newParents.append([branch[0], branch[1]])
                branch[0] = slots[i]
                branch[1] = branch[1] + 1
                if useChallenger:
                    branch[2] = branch[2] + 1
                if makePlots:
                    subPlotLeft.plot([slots[i], slots[i]], [oldParent, slots[i]])
            if makePlots:
                if gamma > 0:
                    trails[oldParent, int(slots[i])] = int(min(slots[i] - oldParent, gamma + 1))
                else:
                    trails[oldParent, int(slots[i])] = int(slots[i] - oldParent)
        if useChallenger:
            def honestTest(hbn):
                out = hbn
                for head in honestHeads:
                    if np.random.uniform(0.0, 1.0) < phi(slots[i] - head[0], head[1]):
                        newParents.append([slots[i], int(head[2] + 1), 0])
                        out = max(hbn, int(head[2] + 1))
                        if makePlots:
                            subPlotLeft.plot([slots[i], slots[i]], [head[0], slots[i]],':')
                return out
            challengerNumber = honestTest(leadingHonestBlockNumber)
            if challengerNumber > leadingHonestBlockNumber:
                leadingHonestBlockNumber = maxBlockNumber
                newHeads = []
                for branch in branches:
                    if branch[1] == leadingHonestBlockNumber:
                        newHeads.append(branch)
                honestHeads = np.empty([1, 3])
                for newHead in newHeads:
                    honestHeads = np.vstack([honestHeads, [newHead[0], (1.0 - alpha) / len(newHeads), newHead[1]]])
        for entry in newParents:
            branches = np.vstack([branches, entry])
        branches = np.unique(branches, axis=0)
        slotSet = set()
        for branch in branches:
            slotSet.add(branch[0])
        branchMaxBlockNumber = {x: -1 for x in slotSet}
        if useChallenger:
            branchReserve = {x: -1 for x in slotSet}
        maxBlockNumber = 0
        for slot in slotSet:
            for entry in branches:
                if entry[0] == slot:
                    if entry[1] > branchMaxBlockNumber[slot]:
                        if useChallenger:
                            branchReserve[slot] = entry[2]
                        branchMaxBlockNumber[slot] = entry[1]
                        maxBlockNumber = max(maxBlockNumber, branchMaxBlockNumber[slot])
        if useChallenger:
            def addReserve(b):
                return np.concatenate((np.asarray(b),[branchReserve[b[0]]]),axis=0)
            branches = np.array(list(map(addReserve,list(filter(lambda x: maxBlockNumber - x[1] < branchDepth,list(branchMaxBlockNumber.items()))))))
        else:
            branches = np.array(list(filter(lambda x: maxBlockNumber - x[1] < branchDepth,list(branchMaxBlockNumber.items()))))
        branches = branches[np.argsort(branches[:, 1])]
        i = i + 1

    # Plot the tracer points of all branches
    if makePlots:
        i = 0
        j = 0
        for n in np.arange(N):
            for m in np.arange(N):
                if gamma > 0:
                    if trails[i, j] < gamma + 1 and trails[i, j] > 0:
                        subPlotLeft.scatter(n, m, s=trails[i, j], c=spectrum[trails[i, j] - 1].reshape(1, -1), alpha=0.5)
                    if trails[i, j] > gamma:
                        subPlotLeft.scatter(n, m, s=int(gamma * fb / fa), c=spectrum[int(gamma * fb / fa)].reshape(1, -1),
                                            alpha=0.5)
                else:
                    if trails[i, j] > 0:
                        subPlotLeft.scatter(n, m, s=1.0, c=spectrum[1].reshape(1, -1), alpha=0.5)
                i = i + 1
            j = j + 1
            i = 0
        subPlotRight.scatter(slots, ys, s=area, c=colors)
        subPlotRight.set_xlabel("Slot")
        subPlotRight.set_ylabel("Y")
        subPlotRight.set_ylim([0.0, 1.0])
        subPlotRight.set_title("Nonce distribution, " + r'$\alpha$ = ' + str(alpha))

    maxL = 0
    numBranch = 0
    for branch in branches:
        maxL = max(branch[1], maxL)
        numBranch = numBranch + 1
    if useChallenger:
        hudStr = ("Maximum block number: " + str(maxL)) + ("\nFinal number of branches: " + str(numBranch)) + (
            "\n[Parent slot, block number, reserve]:\n") + str(branches)
    else:
        hudStr = ("Maximum block number: " + str(maxL)) + ("\nFinal number of branches: " + str(numBranch)) + (
            "\n[Parent slot, block number]:\n") + str(branches)
    if makePlots:
        subPlotLeft.text(0.01, 0.99, hudStr, ha='left', va='top', transform=subPlotLeft.transAxes)
        subPlotLeft.set_xlabel("Slot")
        subPlotLeft.set_ylabel("Parent slot")
        subPlotLeft.set_title("Branching diagram, depth = " + str(branchDepth))
        plt.show()
    else:
        print(hudStr)
    return maxBlockNumber


makePlots = True

notDone = False
seed = 1
print(seed)
max_block_number(ys, 2)
while notDone:
    if max_block_number(ys, 2) > max_block_number(ys, 1):
        notDone = False
        makePlots = True
        print(seed)
        max_block_number(ys, 2)
    else:
        seed = seed + 1
        np.random.seed(seed)
        ys = np.random.rand(N)

