
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

project_to_github = {}

lines = open("github-data.txt").read().split("\n")[1:]
for line in lines:
    line = line.split(' ')
    if len(line) < 2:
        continue
    project_to_github[line[0]] = (int(line[1]), int(line[2]))

lines = open("project_stats.txt").read().split("\n")


leg =  lines[0].split(',')

for i in range(0, len(leg)):
    print i, leg[i]

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

## STARS VS INVARIANTS

cla()

xs = []
ys = []

pset = set()

for project in projects:
    pname = project[0]
    if pname not in pset:
        pset.add(pname)
        # invariant
        xs.append(int(project[3]))
        # stars
        ys.append(project_to_github[pname][0])

plot(ys, xs, 'x')
ylabel("Number of Invariants")
xlabel("Stars")

xscale('log')
yscale('log')

savefig("stars-vs-invariants.pdf")


## STARS VS INVARIANTS/LOC

cla()

xs = []
ys = []

pset = set()

for project in projects:
    pname = project[0]
    if pname not in pset:
        pset.add(pname)
        # invariant
        xs.append(int(project[3])/float(project[10])*1000)
        # stars
        ys.append(project_to_github[pname][0])
plot(ys, xs, 'x')

ylabel("Avg. Invariants per Model")
xlabel("Stars")

xscale('log')
savefig("stars-vs-invariants-per-model.pdf")
