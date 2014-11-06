
import pickle
from collections import defaultdict
from pylab import *
from glob import glob

lw=1
ms=6
fontsize = 7

DISTRIBUTION_NKEYS = 1000

pk_fmts = {"simple_key_value": 'o-', "unique_key_value": 's-'}
pk_colors = {"simple_key_value": 'blue', "unique_key_value": 'green'}
fk_fmts = {"simple": 'o-', "belongs_to": 's-'}
fk_colors = {"simple": 'blue', "belongs_to": 'green'}

relabel = {"simple_key_value": "No validation",
           "unique_key_value": "Validation",
           "simple": "No validation",
           "belongs_to": "Validation"}


PAD_INCHES = 0

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 3.3, 1.4
matplotlib.rcParams['legend.fontsize'] = fontsize

results = []
for r in glob("../results/*.pkl"):
    results += pickle.load(open(r))

pk_results = [r for r in results if r['bench'] == "PK_STRESS"]

#TODO: make into an average`
violations_by_model = defaultdict(lambda: defaultdict(list))
num_dup_keys_by_model = defaultdict(lambda: defaultdict(list))
latencies_by_model = defaultdict(lambda: defaultdict(list))
procs = set()

for r in pk_results:
    for model in r['dups']:
        violations = sum(r[1] for r in r['dups'][model])
        badkeys = len(r['dups'][model])
        num_dup_keys_by_model[model][r['rails_procs']].append(badkeys)
        violations_by_model[model][r['rails_procs']].append(violations)
        latencies_by_model[model][r['rails_procs']].append((average([i.lat_ms for i in r['results'][model][1][0][100:]]), var([i.lat_ms for i in r['results'][model][1][0][100:]])))
        procs.add(r['rails_procs'])

proc_list = list(procs)
proc_list.sort()

pp = []
labels=[]

for model in violations_by_model:

    print model
    for n in proc_list:
        print "LOOK",
        print n, average(violations_by_model[model][n]), average([i[0] for i in latencies_by_model[model][n]]), sqrt(average([i[1] for i in latencies_by_model[model][n][200:]])), average(num_dup_keys_by_model[model][n][200:])

    if model == "indexed_key_value":
        continue
    
    p = plot(range(0, len(proc_list)),
            [average(violations_by_model[model][n]) for n in proc_list],
            pk_fmts[model],
            color=pk_colors[model],
            markerfacecolor="None",
            markeredgecolor=pk_colors[model],
            label=relabel[model])

    pp.append(p[0])
    labels.append(relabel[model])
        
    errorbar(range(0, len(proc_list)),
            [average(violations_by_model[model][n]) for n in proc_list],
            fmt=pk_fmts[model],
            color=pk_colors[model],
            markerfacecolor="None",
            markeredgecolor=pk_colors[model],
            yerr=[std(violations_by_model[model][n]) for n in proc_list],
            label=relabel[model])
    

xticks(range(0, len(proc_list)), [str(i) for i in proc_list])
legend(pp, labels, loc="lower right", frameon=False, numpoints=1)
xlabel("Number of Rails Processes")
ylabel("Number of Duplicate Records")
gca().set_yscale('symlog')
xlim(xmax=len(proc_list)-1)
        
savefig("pk_stress_violations.pdf", bbox_inches="tight")

#####

workloads = unique([r['workload'] for r in results if r['bench'] == 'PK_WORKLOAD'])

for workload in workloads:
    cla()
    print workload

    pk_results = [r for r in results if r['bench'] == "PK_WORKLOAD" and r['workload'] == workload]


    violations_by_model = defaultdict(lambda: defaultdict(list))
    latencies_by_model = defaultdict(lambda: defaultdict(list))
    num_dup_keys_by_model = defaultdict(lambda: defaultdict(list))    
    procs = set()

    for r in pk_results:
        for model in r['dups']:
            violations = sum(r[1] for r in r['dups'][model])
            violations_by_model[model][r['records']].append(violations)
            badkeys = len(r['dups'][model])
            num_dup_keys_by_model[model][r['records']].append(badkeys)         
            latencies_by_model[model][r['records']].append(average([i.lat_ms for i in r['results'][model][1]]))
            procs.add(r['records'])

    proc_list = list(procs)
    proc_list.sort()

    for model in violations_by_model:
        if model == "indexed_key_value":
            continue
        
        errorbar(range(0, len(proc_list)),
                [average(violations_by_model[model][n]) for n in proc_list],
                fmt=pk_fmts[model],
                color=pk_colors[model],
                markerfacecolor="None",
                markeredgecolor=pk_colors[model],
                yerr=[std(violations_by_model[model][n]) for n in proc_list],
                label=relabel[model])

        print model
        for n in proc_list:
            print n, average(violations_by_model[model][n]), average(latencies_by_model[model][n]), average(num_dup_keys_by_model[model][n])

        if workload == "linkbench-upd":
            labels =  ["1", "10", "100", "1K", "10K", "100K", "1M"]
        else:
            labels = ["", "", "", "", "", "", ""]
        xticks(range(0, len(proc_list)), labels)
    #legend(loc="lower right")
    
    #xlabel("Number of Possible Keys")
    if(workload == "linkbench-upd"):
        xlabel("Number of Possible Keys")

    workload_to_label = {"ycsb": "YCSB",
                         "uniform": "Uniform",
                         "linkbench-upd": "LinkBench-Update",
                         "linkbench-ins": "LinkBench-Insert"}
        
    title(workload_to_label[workload], fontsize=fontsize)
    ylim(ymin=0, ymax=10000)
    gca().set_yscale('symlog')

    pp = []
    labels = []

    if workload == "uniform":
        for m in ['simple_key_value', 'unique_key_value']:
            pp.append(plot([0, -100], pk_fmts[m], color=pk_colors[m], markerfacecolor="None", markeredgecolor=pk_colors[m])[0])
            labels.append(relabel[m])
        legend(pp, labels, loc=(.04, .5), frameon=False, numpoints=1)

    #title(workload)
    subplots_adjust(bottom=.26, right=0.95, top=0.87, left=.18)        
    savefig("pk-workload-%s-violations.pdf" % (workload), transparent=True)

    cla()
    continue

    # find out all the duplicate keys for the validator-based implementaton
    dup_lists_for_plot = [r['dups']['uniform_key_value'] for r in pk_results if r['records'] == DISTRIBUTION_NKEYS and r['workload'] == workload]

    dup_list_for_plot = defaultdict(int)
    
    # now add up all of the duplicate key entries, normalizing for number of entries
    for run in dup_list_for_plot:
        for pair in run:
            dup_lists_for_plot[int(pair[0])] += pair[1]/float(len(dup_lists_for_plot))


    cla()
    xs = range(0, DISTRIBUTION_NKEYS)
    bar(xs, [dup_lists_for_plot[i] for i in xs])
    xlabel("key")
    ylabel("number of duplicate entries")
    savefig("pk-dups-by-key-%s.pdf" % (workload), bbox_inches="tight")

####


fk_results = [r for r in results if r['bench'] == "FK_WORKLOAD"]

cla()
violations_by_model = defaultdict(lambda: defaultdict(list))
latencies_by_model = defaultdict(lambda: defaultdict(list))
procs = set()

for r in fk_results:
    for model in r['dups']:
        violations = sum(r[1] for r in r['dups'][model])
        violations_by_model[model][r['records']].append(violations)
        latencies_by_model[model][r['records']].append((average([i.lat_ms for i in r['results'][model][1][200+r['records']:]]), var([i.lat_ms for i in r['results'][model][1][200+r['records']:]])))
        procs.add(r['records'])

proc_list = list(procs)
proc_list.sort()

pp = []
labels=[]

for model in violations_by_model:
    print model
    for n in proc_list:
        print "LOOK",        
        print n, average(violations_by_model[model][n]), average([i[0] for i in latencies_by_model[model][n]]), sqrt(average([i[1] for i in latencies_by_model[model][n]]))
    
    if model == "dbfk":
        continue

    p = plot(range(0, len(proc_list)),
                [average(violations_by_model[model][n]) for n in proc_list],
                fk_fmts[model],
                color=fk_colors[model],
                markerfacecolor="None",
                markeredgecolor=fk_colors[model],
                label=relabel[model])
    pp.append(p[0])
    labels.append(relabel[model])

    

    errorbar(range(0, len(proc_list)),
                [average(violations_by_model[model][n]) for n in proc_list],
                fmt=fk_fmts[model],
                color=fk_colors[model],
                markerfacecolor="None",
                markeredgecolor=fk_colors[model],
                yerr=[std(violations_by_model[model][n]) for n in proc_list],
                label=relabel[model])


xticks(range(0, len(proc_list)), [str(int(i/10.)) for i in proc_list])
legend(pp, labels, loc="lower left", frameon=False, numpoints=1)
xlabel("Number of Departments")
ylabel("Number of Orphaned Users")

gca().set_yscale('symlog')

        
savefig("fk-workload-violations.pdf", bbox_inches="tight")


####


fk_results = [r for r in results if r['bench'] == "FK_STRESS"]

cla()
violations_by_model = defaultdict(lambda: defaultdict(list))
latencies_by_model = defaultdict(lambda: defaultdict(list))
procs = set()

for r in fk_results:
    for model in r['dangling']:
        violations = sum(r[1] for r in r['dangling'][model])
        violations_by_model[model][r['rails_procs']].append(violations)
        latencies_by_model[model][r['rails_procs']].append(average([i.lat_ms for i in r['results'][model][1][0]]))
        procs.add(r['rails_procs'])

proc_list = list(procs)
proc_list.sort()

pp = []
labels = []

for model in violations_by_model:
    print model
    for n in proc_list:
        print n, average(violations_by_model[model][n]), average(latencies_by_model[model][n])

    
    if model == "dbfk":
        continue

    p = plot(range(0, len(proc_list)),
                [average(violations_by_model[model][n]) for n in proc_list],
                fk_fmts[model],
                color=fk_colors[model],
                markerfacecolor="None",
                markeredgecolor=fk_colors[model],
                label=relabel[model])
    pp.append(p[0])
    labels.append(relabel[model])

    
    errorbar(range(0, len(proc_list)),
                [average(violations_by_model[model][n]) for n in proc_list],
                fmt=fk_fmts[model],
                color=fk_colors[model],
                markerfacecolor="None",
                markeredgecolor=fk_colors[model],
                yerr=[std(violations_by_model[model][n]) for n in proc_list],
                label=relabel[model])


xticks(range(0, len(proc_list)), [str(i) for i in proc_list])
xlim(xmax=len(proc_list)-1)

print pp

legend(pp, labels, loc="lower right", frameon=False, numpoints=1)
xlabel("Number of Rails Workers")
ylabel("Number of Orphaned Users")

gca().set_yscale('symlog')
subplots_adjust(bottom=.26, right=0.95, top=0.9, left=.18)                
savefig("fk-stress-violations.pdf", bbox_inches="tight")
