
import pickle
from collections import defaultdict
from pylab import *
from glob import glob
from itertools import groupby

lw=1
ms=6
fontsize = 7.5

optimistic_locks = defaultdict(int)

optimistic_locks['canvas-lms'] = 1
optimistic_locks['chiliproject'] = 1
optimistic_locks['openproject']=3
optimistic_locks['radiant'] = 1
optimistic_locks['redmine'] = 1

DO_PRINT_TABLE = True

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 3.3, 1.4
matplotlib.rcParams['legend.fontsize'] = fontsize

project_to_github = {}

lines = open("github-data.txt").read().split("\n")[1:]
for line in lines:
    lines = line.split(' ')
    if len(lines) < 2:
        continue
    stars = int(lines[1])
    watchers = int(lines[2])
    desc = line.split('"')[1].split('"')[0]
    fullname = line.split('"')[3].split('"')[0]
    project_to_github[lines[0]] = (stars, watchers, desc, fullname)

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

#for project in projects:
#    print project[0], project[3], project[6], project[11], project[12]

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

subplots_adjust(bottom=.27, right=0.95, top=0.9, left=.18)
tick_params(axis='x',which='both',bottom='off')
savefig("normalized-project-bar.pdf", pad_inches=.25)

#print sum([int(p[2]) for p in projects])

## STARS VS INVARIANTS

cla()

xs = []
ys = []

pset = set()

for project in projects:
    pname = project[0]
    if pname not in project_to_github:
        continue
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
    if pname not in project_to_github:
        print "MISSING STARS:", pname
        continue
    
    if pname not in pset:
        pset.add(pname)
        # invariant
        if float(project[10]) > 0:
            #print pname, int(project[3])/float(project[10]), project[10]
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
            #print pname, int(project[3])/float(project[10]), project[9]
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
    
        

clf()


#(name, nauthors, nlines, nvalidations, nbuiltin, ncustom, nassociations, nbv_callbacks, nac_callbacks)

DO_NORMALIZE = True
n_model_offset = 10

#sort by nvalidations + nassociations
if DO_NORMALIZE:
    projects.sort(key = lambda x: -int(x[3])/float(x[10]))
else:
    projects.sort(key = lambda x: -int(x[3]))

projects.sort(key = lambda x: -int(x[n_model_offset]))


toplot = [(11, "purple", "Locks", DO_NORMALIZE),
 (12, "red", "Transactions", DO_NORMALIZE),
 (6, "green", "Associations", DO_NORMALIZE),
 (3, "blue", "Validations", DO_NORMALIZE),
 (2, "blue", "Invariants", DO_NORMALIZE),
 (n_model_offset, "orange", "Models", False)]


TARGET = -1
print projects[TARGET], projects[TARGET][3], float(projects[TARGET][3])/float(projects[TARGET][n_model_offset])

for p in projects:
    print "    ".join([p[0], str(int(p[3])/float(p[n_model_offset])), p[3], p[n_model_offset]])

print "TOTAL_COMMITS: ", sum([int(p[9]) for p in projects]), average([int(p[9]) for p in projects]), std([int(p[9]) for p in projects]), median([int(p[9]) for p in projects])
print "TOTAL_LOC: ", sum([int(p[2]) for p in projects]),  average([int(p[2]) for p in projects]),  std([int(p[2]) for p in projects]),  median([int(p[2]) for p in projects])
print "TOTAL_AUTHORS: ", sum([int(p[1]) for p in projects]),  average([int(p[1]) for p in projects]),  std([int(p[1]) for p in projects]),  median([int(p[1]) for p in projects])
    
for p in toplot:
    offset, color, label, normalized = p

    # sad panda
    if label == "Invariants":
        ys = [(int(projects[i][3])+int(projects[i][6]))/float(projects[i][n_model_offset]) for i in range(0, len(projects))]
    else:
        if normalized:
            ys =  [int(projects[i][offset])/float(projects[i][n_model_offset]) for i in range(0, len(projects))]
        else:
            ys =  [int(projects[i][offset]) for i in range(0, len(projects))]

    avg = average(ys)
    print label, max(ys)
    
    bar(range(1, len(projects)+1), ys, color=color, label=label, edgecolor="None", linewidth=0, zorder=10)
    plot(range(0, len(projects)+1), [avg for i in range(0, len(projects)+1)], ':', color = "gray", zorder=0)

    #legend(loc="upper right", frameon=False, numpoints=0)
    xlim(xmax=len(projects)+1)

    N_YMAX = 8

    if label == "Models":
        yticks([0, 30, 60, 90, 120, 150, 180])
    
    if normalized:
        ylim(ymax=N_YMAX)

        #yticks([0, 1, 2, 3, 4, 5, 6, 7, 8], ["0", "", "2", "", "4", "", "6", "", "8"])
        yticks([0, 2,4,6,8])

        print ys[-2]
        if ys[-2] > N_YMAX:
            
            text(61.5, 9.45, str(ys[-2]), size=4)
            plot([65, 66], [9.65, 9.65], '-', color="black", linewidth=.25)

    if label == "Invariants":
        ylabel("Constraints/Table")
        #print "AVERAGES:", avg(ys)
        for i in range(0, len(ys)):
            if ys[i] > 10:
                print i, ys[i]
    else:
        ylabel("%s%s" % (label, "/Model" if normalized else ""))
    gca().spines['top'].set_visible(False)
    gca().spines['right'].set_visible(False)
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    gca().xaxis.set_tick_params(width=0)
    if label == "Associations":
        print "MAXXX", max(ys)
        xticks([i*10 for i in range(0, 7)])
        xlabel("Project Number")
    else:
        xticks([i*10 for i in range(0, 7)], ["" for i in range(0, 7)])
    subplots_adjust(bottom=.23, right=0.95, top=0.9, left=.12)        
    savefig(label.lower()+"-single-bar.pdf", transparent=True)
    cla()

print "NUM PROJECTS WITH LOCKS:", len([o for o in projects if int(o[11]) != 0])
print "NUM PROJECTS WITH TXNS:", len([o for o in projects if int(o[12]) != 0])
    
if DO_PRINT_TABLE:
    from os import system
    import datetime

    output = []

    for p in projects:
        name = p[0]
        fullname = project_to_github[name][3]
        desc = project_to_github[name][2]
        stars = project_to_github[name][0]
        watchers = project_to_github[name][1]        
        num_authors = p[1]
        numlines_ruby = p[2]
        num_validations = p[3]
        num_associations = p[6]
        num_commits = p[9]
        num_models = p[10]
        num_locks = p[11]
        o_locks = optimistic_locks[name]
        num_transactions = p[12]

        system("cd ../"+name+"; git log -n 1 --pretty='%h %at' > /tmp/hash.txt")
        githash, timestr = open("/tmp/hash.txt").read().split(' ')
        output.append([fullname,
                       "{\\scriptsize{%s}}" % (desc),
                       num_authors,
                       numlines_ruby,
                       num_commits,
                       num_models,
                       num_transactions,
                       num_locks,
                       o_locks,
                       num_validations,
                       num_associations,
                       stars,
                       "{\\tiny\\texttt{%s}}" % (githash),
                       int(timestr)])

    avgs = []
    for i in range(0, len(output[0])):
        if i == 0:
            avgs.append("\\textbf{Average:}")
        elif i < 2 or (i > len(output[0])-3 and i != len(output[0])-1):
            avgs.append("")
        elif i == len(output[0]) - 1:
            avgs.append("{\\tiny\\textbf{%s}}" % (datetime.datetime.fromtimestamp(average([o[i] for o in output])).strftime("%m/%d/%y")))
        else:
            avgs.append("\\textbf{%s}" % ("{0:,.2f}".format(average([float(o[i]) for o in output]))))
    output.append(avgs)

    for o in output[:-1]:
        for i in range(2, len(o)-2):
            o[i] = "{:,}".format(int(o[i]))
        o[-1] = "{\\tiny{%s}}" % datetime.datetime.fromtimestamp(o[-1]).strftime("%m/%d/%y")



    output.insert(0, ["Name",
                      "Description",
                       "Num. Authors",
                       "LoC Ruby",
                       "Num. Commits",
                       "Num. Models",
                       "Num. Transactions",
                       "PL",
                       "OL",
                       "V",
                       "A",
                       "GitHub Stars",
                       "Githash",
                       "Last commit date"])
            
    for o in output:
        print " & ".join([str(i) for i in o])+"\\\\"


                       
                       
