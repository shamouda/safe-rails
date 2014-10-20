
import pickle
from collections import defaultdict
from pylab import *
from glob import glob
from itertools import groupby

lw=1
ms=6
fontsize = 7

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 3.5, 1.7
matplotlib.rcParams['legend.fontsize'] = fontsize

lines = open("project_stats.txt").read().split("\n")
print lines[0]
lines = lines[1:]

projects = []

#(name, nauthors, nlines, nvalidations, nbuiltin, ncustom, nassociations, nbv_callbacks, nac_callbacks)
for line in lines:
    line = line.split(',')
    if len(line) > 1:
        projects.append(line)

#sort by nvalidations + nassociations
projects.sort(key = lambda x: int(x[3])+int(x[6]))
projects.reverse()

print projects

bar(range(1, len(projects)+1), [int(projects[i][3])+int(projects[i][6]) for i in range(0, len(projects))], color="green", label="Associations", edgecolor="None", linewidth=0)
bar(range(1, len(projects)+1), [int(projects[i][3]) for i in range(0, len(projects))], color="blue", label="Validations", edgecolor="None", linewidth=0)

xticks([i*10 for i in range(0, 6)], ["" for i in range(0, 6)])

legend(loc="upper right", frameon=False)


ylabel("Total Usages")
xlim(xmax=53)

subplots_adjust(bottom=.24, right=0.95, top=0.9, left=.18)
tick_params(axis='x',which='both',bottom='off')
savefig("by-project-bar.pdf", pad_inches=.25)

cla()

bar(range(1, len(projects)+1), [(int(projects[i][3])+int(projects[i][6]))/float(projects[i][2])*1000 for i in range(0, len(projects))], color="green", edgecolor="None")
bar(range(1, len(projects)+1), [int(projects[i][3])/float(projects[i][2])*1000 for i in range(0, len(projects))], color="blue", edgecolor="None")

ylabel("Usages per KLoC")
xlabel("Project ID")
xlim(xmax=53)

subplots_adjust(bottom=.24, right=0.95, top=0.9, left=.18)
tick_params(axis='x',which='both',bottom='off')
savefig("normalized-project-bar.pdf", pad_inches=.25)

print sum([int(p[2]) for p in projects])

