
import pickle
from collections import defaultdict
from pylab import *
from glob import glob
from itertools import groupby

lw=1
ms=8
fontsize = 8

fmts = ['-', '--', '-.', ':']

# super inefficient
def interpolate(target_xs, actual_xs, actual_ys):
    return_ys = []
    for x in target_xs:
        idx = 0
        while True:
            # if we are at the end of the list
            if idx == len(actual_xs):
                below_x = actual_xs[-1]
                below_y = actual_ys[-1]
                above_x = 1
                above_y = 1
                break

            if x < actual_xs[idx]:
                idx = 0
                below_x = 0
                below_y = 0
                above_x = actual_xs[idx]
                above_y = actual_ys[idx]
                break
            
            if x > actual_xs[idx]:
                below_x = actual_xs[idx]
                below_y = actual_ys[idx]
                if idx+1 == len(actual_xs):
                    above_x = 1
                    above_y = 1
                    break
                elif x <= actual_xs[idx+1]:
                    above_x = actual_xs[idx+1]
                    above_y = actual_ys[idx+1]
                    break
            idx += 1
        
        # interpolate
        interpolated_y = below_y+(above_y-below_y)*(x-below_x)/(above_x-below_x)
        if x == 1 and interpolated_y == 0:
            print actual_ys
        return_ys.append(interpolated_y)
    return return_ys

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 3.5, 2.1
matplotlib.rcParams['legend.fontsize'] = fontsize

lines = open("historical.txt").read().split("\n")

leg =  lines[0].split(',')

for i in range(0, len(leg)):
    print i, leg[i]

lines = lines[1:]

projects = defaultdict(list)

for line in lines:
    if len(line) <= 1:
        continue
    line = line.split(',')
    # reverse commit number
    line[1] = int(line[2])-int(line[1])
    projects[line[0]].append(line)

xmarks = [i/100. for i in xrange(1, 101, 4)]+[1.]
print xmarks

all_txn_pcts = []
all_invariant_pcts = []
all_association_pcts = []
all_model_pcts = []

for p in projects:
    commits = projects[p]
    commits.sort(key = lambda x: int(x[1]))

    commit_pcts = [float(i[1])/float(i[2]) for i in commits]

    tot_models = float(commits[-1][12])
    if tot_models == 0:
        continue
    
    tot_txns = float(commits[-1][14])
    if tot_txns != 0:
        txn_pcts = interpolate(xmarks,
                            commit_pcts,
                           [int(i[14])/tot_txns*int(i[12])/tot_models for i in commits])
        all_txn_pcts.append(txn_pcts)
    #else:
    #    all_txn_pcts.append([1 for i in xmarks])

    model_pcts = interpolate(xmarks,
                            commit_pcts,
                           [int(i[12])/tot_models for i in commits])
    all_model_pcts.append(model_pcts)


    tot_invariants = max(float(commits[-1][6]), 0)
    if tot_invariants != 0:
        invariant_pcts = interpolate(xmarks,
                                    commit_pcts,
                                    [int(i[6])/tot_invariants*int(i[12])/tot_models for i in commits])
        all_invariant_pcts.append(invariant_pcts)
    else:
        print p
    #else:
    #    all_invariant_pcts.append([1 for i in xmarks])

    tot_associations = max(float(commits[-1][9]), 0)
    if tot_associations != 0:
        association_pcts = interpolate(xmarks,
                                    commit_pcts,
                                   [int(i[9])/tot_associations*int(i[12])/tot_models for i in commits])
        all_association_pcts.append(association_pcts)
    #else:
    #    all_association_pcts.append([1 for i in xmarks])

metric = median

plot([x*100 for x in xmarks], [metric([t[i] for t in all_model_pcts])*100. for i in range(0, len(xmarks))], '-', label="Models", color="c")
plot([x*100 for x in xmarks], [metric([t[i] for t in all_association_pcts])*100. for i in range(0, len(xmarks))], '--', label="Associations per Model", color="blue")
plot([x*100 for x in xmarks], [metric([t[i] for t in all_invariant_pcts])*100. for i in range(0, len(xmarks))], '.-', label="Validations per Model", markersize=5, color="green")
plot([x*100 for x in xmarks], [metric([t[i] for t in all_txn_pcts])*100. for i in range(0, len(xmarks))], '-s', label="Transactions per Model", markersize=3, markeredgecolor="None", color="red")


ylabel("\% of Final Occurrences")
ylim(ymin=0, ymax=100)
xlabel("Normalized Application History (\% of Commits)")

legend(loc="lower right", frameon=False)

subplots_adjust(bottom=.22, right=0.95, top=0.9, left=.15)
savefig("historical-median.pdf")

    

    
    
