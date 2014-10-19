
from pylab import *

xs = []
ys = []

lw=1
ms=6
fontsize = 8

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 3.3, 1.5
matplotlib.rcParams['legend.fontsize'] = fontsize

lines = open("authors.txt").read().split("\n")
print lines[0]
lines = lines[1:]

# project, author, invariants_written, author_lines_inserted, author_lines_deleted, total_invariants, total_lines_inserted, total_lines_deleted, author_commits, total_commits

authors = []

for line in lines:
    line = line.split(',')
    if len(line) < 2:
        continue
    authors.append(line)

for a in authors:
    if a[2].find("Raphael") != -1:
        print a
    
author_invariant_prop = [int(a[2])/float(a[5])*100 for a in authors]
author_loc_prop = [(int(a[3])+int(a[4]))/(float(a[6])+float(a[7]))*100 for a in authors]
author_commit_prop = [int(a[8])/float(a[9])*100 for a in authors]


plot(author_invariant_prop, author_loc_prop, 'x')
plot([0, 100], [0, 100], color="grey")
xlabel("Invariants written (%)")
ylabel("Lines contributed (%)")

subplots_adjust(bottom=.24, right=0.95, top=0.9, left=.18)
savefig("author-inv-vs-loc.pdf")

cla()

plot(author_invariant_prop, author_commit_prop, 'x')
plot([0, 100], [0, 100], color="grey")
xlabel("Invariants written (%)")
ylabel("Commits (%)")

subplots_adjust(bottom=.24, right=0.95, top=0.9, left=.18)
savefig("author-inv-vs-commits.pdf")

### print suspicious committers
for a in authors:
    this_invariant_prop = int(a[2])/float(a[5])*100 
    this_loc_prop = (int(a[3])+int(a[4]))/(float(a[6])+float(a[7]))*100
    if this_invariant_prop == 0 and this_loc_prop > 75:
        print this_invariant_prop, this_loc_prop, a

### figure out how many are above line
more_invs_than_commits = 0
more_invs_than_locs = 0

more_invs_than_commits_excl_zero = 0
more_invs_than_locs_excl_zero = 0
num_nonzero_invs = 0
for a in authors:
    this_invariant_prop = int(a[2])/float(a[5])*100 
    this_loc_prop = (int(a[3])+int(a[4]))/(float(a[6])+float(a[7]))*100
    this_commit_prop = (int(a[8]))/(float(a[9]))*100        
    if this_invariant_prop > this_commit_prop:
        more_invs_than_commits += 1
    if this_invariant_prop > this_loc_prop:
        more_invs_than_locs += 1

    if this_invariant_prop > 0:
        num_nonzero_invs += 1
        if this_invariant_prop > this_commit_prop:
            more_invs_than_commits_excl_zero += 1
        if this_invariant_prop > this_loc_prop:
            more_invs_than_locs_excl_zero += 1
            
print "------"
print "PERCENT MORE INVS THAN COMMITS:", more_invs_than_commits/float(len(authors))
print "PERCENT MORE INVS THAN COMMITS (excl zero):", more_invs_than_commits_excl_zero/float(num_nonzero_invs)
print

print "PERCENT MORE INVS THAN LOCS", more_invs_than_locs/float(len(authors))
print "PERCENT MORE INVS THAN LOCS (excl zero):", more_invs_than_locs_excl_zero/float(num_nonzero_invs)
print
