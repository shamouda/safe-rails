
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
projects.sort(key = lambda x: int(x[3])+int(x[6])+int(x[11])+int(x[12]))
projects.reverse()

bar(range(1, len(projects)+1), [int(projects[i][3])+int(projects[i][6])+int(projects[i][12])+int(projects[i][11]) for i in range(0, len(projects))], color="purple", label="Locks", edgecolor="None", linewidth=0)
bar(range(1, len(projects)+1), [int(projects[i][3])+int(projects[i][6])+int(projects[i][12]) for i in range(0, len(projects))], color="red", label="Transactions", edgecolor="None", linewidth=0)
bar(range(1, len(projects)+1), [int(projects[i][3])+int(projects[i][6]) for i in range(0, len(projects))], color="green", label="Associations", edgecolor="None", linewidth=0)
bar(range(1, len(projects)+1), [int(projects[i][3]) for i in range(0, len(projects))], color="blue", label="Validations", edgecolor="None", linewidth=0)

for project in projects:
    print project[0], project[3], project[6], project[11], project[12]

xticks([i*10 for i in range(0, 6)], ["" for i in range(0, 6)])

legend(loc="upper right", frameon=False)


ylabel("Total Usages")
xlim(xmax=53)

subplots_adjust(bottom=.24, right=0.95, top=0.9, left=.18)
tick_params(axis='x',which='both',bottom='off')
savefig("by-project-bar.pdf", pad_inches=.25)

cla()
bar(range(1, len(projects)+1), [(int(projects[i][3])+int(projects[i][6])+int(projects[i][12])+int(projects[i][11]))/float(projects[i][2])*1000 for i in range(0, len(projects))], color="purple", label="Transactions", edgecolor="None", linewidth=0)
bar(range(1, len(projects)+1), [(int(projects[i][3])+int(projects[i][6])+int(projects[i][12]))/float(projects[i][2])*1000 for i in range(0, len(projects))], color="red", label="Transactions", edgecolor="None", linewidth=0)
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
        if float(project[10]) > 0:
            print pname, int(project[3])/float(project[10]), project[10]
            xs.append(int(project[3])/float(project[10]))
        else:
            xs.append(0)
        # stars
        ys.append(project_to_github[pname][0])
plot(ys, xs, 'x')

ylabel("Avg. Invariants per Model")
xlabel("Stars")

xscale('log')
savefig("stars-vs-invariants-per-model.pdf")


cla()

xs = []
ys = []
pset = set()

for project in projects:
    pname = project[0]
    if pname not in pset:
        pset.add(pname)
        # invariant
        if float(project[10]) > 0:
            print pname, int(project[3])/float(project[10]), project[9]
            xs.append(int(project[3])/float(project[10]))
        else:
            xs.append(0)
        # stars
        ys.append(int(project[9]))
plot(ys, xs, 'x')

ylabel("Avg. Invariants per Model")
xlabel("Commits per Model")

xscale('log')
savefig("commits-vs-invariants-per-model.pdf")


### broken-down bar plots

for p in projects:
    if p[10] == "0":
        print p[0]
# tmp fix
projects = [p for p in projects if p[10] != "0"]
    
        
#sort by nvalidations + nassociations
projects.sort(key = lambda x: int(x[3])/float(x[10]))
projects.reverse()

clf()
from pylab import *
matplotlib.rcParams['figure.figsize'] = 3.5, 1


#(name, nauthors, nlines, nvalidations, nbuiltin, ncustom, nassociations, nbv_callbacks, nac_callbacks)

n_model_offset = 10
toplot = [(11, "purple", "Locks"),
 (12, "red", "Transactions"),
 (6, "green", "Associations"),
 (3, "blue", "Validations")]


print projects[-5], projects[-5][3], float(projects[-5][3])/float(projects[-5][n_model_offset])
    
for p in toplot:
    offset, color, label = p
    bar(range(1, len(projects)+1), [int(projects[i][offset])/float(projects[i][n_model_offset]) for i in range(0, len(projects))], color=color, label=label, edgecolor="None", linewidth=0)
    #legend(loc="upper right", frameon=False, numpoints=0)
    xlim(xmax=len(projects))
    ylim(ymax=7)
    ylabel("%ss per Model" % (label))
    gca().spines['top'].set_visible(False)
    gca().spines['right'].set_visible(False)
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    gca().xaxis.set_tick_params(width=0)
    if label == "Transactions":
        xticks([i*10 for i in range(0, 5)])
        xlabel("Project Number")
    else:
        xticks([i*10 for i in range(0, 5)], ["" for i in range(0, 5)])        
    savefig(label.lower()+"-single-bar.pdf")
    cla()

