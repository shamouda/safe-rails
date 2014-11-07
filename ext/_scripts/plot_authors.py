
from pylab import *
from collections import defaultdict
from scipy import stats

xs = []
ys = []

lw=1
ms=6
fontsize = 6.5

matplotlib.rcParams['lines.linewidth'] = lw
matplotlib.rcParams['axes.linewidth'] = lw
matplotlib.rcParams['lines.markeredgewidth'] = lw
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['font.size'] = fontsize
matplotlib.rcParams['font.weight'] = 'normal'
matplotlib.rcParams['figure.figsize'] = 3.3, 1.6
matplotlib.rcParams['legend.fontsize'] = fontsize

ALPHA=.5

lines = open("authors.txt").read().split("\n")
print ",".join(lines[0].split("\t"))
lines = lines[1:]

# project, author, invariants_written, author_lines_inserted, author_lines_deleted, total_invariants, total_lines_inserted, total_lines_deletedd, author_commits, total_commits

authors = []

for line in lines:
    line = line.split('\t')
    if len(line) < 2:
        continue
    authors.append(line)

author_invariant_prop = [int(a[2])/float(a[5])*100 for a in authors]
author_loc_prop = [(int(a[3])+int(a[4]))/(float(a[6])+float(a[7]))*100 for a in authors]
author_commit_prop = [int(a[8])/float(a[9])*100 for a in authors]


plot(author_invariant_prop, author_loc_prop, 'x')
plot([0, 100], [0, 100], color="grey", linewidth=lw/2.)
xlabel("Invariants written (%)")
ylabel("Lines contributed (%)")

subplots_adjust(bottom=.24, right=0.95, top=0.9, left=.18)
savefig("author-inv-vs-loc.pdf")

cla()

plot(author_invariant_prop, author_commit_prop, 'x', alpha=ALPHA)
plot([0, 100], [0, 100], color="grey", linewidth=lw/2.)
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


cla()
authors_by_project = defaultdict(list)
for author in authors:
    authors_by_project[author[0]].append(author)

project_curves = {}
for p in authors_by_project:
    project_authors = authors_by_project[p]
    project_authors.sort(key = lambda x: int(x[2]))
    project_authors.reverse()
    total_invariants = float(project_authors[0][5])

    cdf = [0]
    cum = 0
    for author in project_authors:
        t = int(author[2])/total_invariants
        cum += t
        cdf.append(cum)
    if cum < .999:
        print cum, p, project_authors[0][5], sum([int(author[2]) for author in project_authors])
        for author in project_authors:
            continue
            if int(author[2])> 0:
                print author, author[2]


    xs = [i/float(len(project_authors)) for i in range(0, len(project_authors)+1)]
    project_curves[p] = (xs, cdf)      
    plot(xs, cdf, color='#555555', alpha=.3, linewidth=lw/2.)

# calculate average CDF

xs = [i/1000. for i in range(1, 1000)]
avg_ys = [0]
for x in xs:
    this_sum = 0
    for p in project_curves:
        p_xs, p_ys = project_curves[p]
        idx = 0
        while True:
            if idx == len(p_xs):
                below_x = p_xs[-1]
                below_y = p_ys[-1]
                above_x = 1
                above_y = 1
                break

            if x < p_xs[idx]:
                idx = 0
                below_x = 0
                below_y = 0
                above_x = p_xs[idx]
                above_y = p_ys[idx]
                break
            
            if x > p_xs[idx]:
                below_x = p_xs[idx]
                below_y = p_ys[idx]
                if idx+1 == len(p_xs):
                    above_x = 1
                    above_y = 1
                    break
                elif x <= p_xs[idx+1]:
                    above_x = p_xs[idx+1]
                    above_y = p_ys[idx+1]
                    break
            idx += 1
        
        # interpolate
        interpolated_y = below_y+(above_y-below_y)*(x-below_x)/(above_x-below_x)
        this_sum += interpolated_y

    y = this_sum/float(len(project_curves))
    avg_ys.append(y)

ys_of_interest = [.95]#[.5, .95]

for yi in ys_of_interest:
    for i in range(0, len(avg_ys)):
        if yi < avg_ys[i]:
            above_y = avg_ys[i]
            below_y = avg_ys[i-1]
            above_x = xs[i]
            below_x = xs[i-1]
            
            interpolated_x = below_x+(above_x-below_x)*(yi-below_y)/(above_y-below_y)
            break
    print yi, interpolated_x
    plot([interpolated_x, interpolated_x], [0, yi], ':', color="black")
    plot([0, interpolated_x], [yi, yi], ':', color="black")    

    
xlabel("Proportion Authors")
ylabel("Valid/Assoc Authored (CDF)")

#xlim(xmax=.4)
ylim(ymax=1)

plot([0]+xs, avg_ys, color="red", linewidth=lw*1.5)

savefig("invariant-authorship-cdf.pdf")


cla()

project_curves = {}
for p in authors_by_project:
    project_authors = authors_by_project[p]
    project_authors.sort(key = lambda x: int(x[8]))
    project_authors.reverse()
    total_invariants = float(project_authors[0][9])

    cdf = [0]
    cum = 0
    for author in project_authors:
        t = int(author[8])/total_invariants
        cum += t
        cdf.append(cum)
    if cum < .999:
        print cum, p, project_authors[0][9], sum([int(author[8]) for author in project_authors])

    xs = [i/float(len(project_authors)) for i in range(0, len(project_authors)+1)]
    project_curves[p] = (xs, cdf)      
    plot(xs, cdf, color='#555555', alpha=.3, linewidth=lw/2.)

# calculate average CDF

xs = [i/1000. for i in range(1, 1000)]
avg_ys = [0]
for x in xs:
    this_sum = 0
    for p in project_curves:
        p_xs, p_ys = project_curves[p]
        idx = 0
        while True:
            if idx == len(p_xs):
                below_x = p_xs[-1]
                below_y = p_ys[-1]
                above_x = 1
                above_y = 1
                break

            if x < p_xs[idx]:
                idx = 0
                below_x = 0
                below_y = 0
                above_x = p_xs[idx]
                above_y = p_ys[idx]
                break
            
            if x > p_xs[idx]:
                below_x = p_xs[idx]
                below_y = p_ys[idx]
                if idx+1 == len(p_xs):
                    above_x = 1
                    above_y = 1
                    break
                elif x <= p_xs[idx+1]:
                    above_x = p_xs[idx+1]
                    above_y = p_ys[idx+1]
                    break
            idx += 1
        
        # interpolate
        interpolated_y = below_y+(above_y-below_y)*(x-below_x)/(above_x-below_x)
        this_sum += interpolated_y

    avg_ys.append(this_sum/float(len(project_curves)))

ys_of_interest = [.95]#[.5, .95]

for yi in ys_of_interest:
    for i in range(0, len(avg_ys)):
        if yi < avg_ys[i]:
            above_y = avg_ys[i]
            below_y = avg_ys[i-1]
            above_x = xs[i]
            below_x = xs[i-1]
            
            interpolated_x = below_x+(above_x-below_x)*(yi-below_y)/(above_y-below_y)
            break
    print yi, interpolated_x
    plot([interpolated_x, interpolated_x], [0, yi], ':', color="black")
    plot([0, interpolated_x], [yi, yi], ':', color="black")    

    
plot([0]+xs, avg_ys, color="red", linewidth=lw*1.5)

#xlabel("Percentage of Authors")
ylabel("Commits Authored (CDF)")

#xlim(xmax=.4)
ylim(ymax=1)

savefig("commit-authorship-cdf.pdf")


# project, author, invariants_written, author_lines_inserted, author_lines_deleted, total_invariants, total_lines_inserted, total_lines_deleted, author_commits, total_commits

loc_ranks = []
commit_ranks = []
invariant_ranks = []

for p in authors_by_project:
    project = authors_by_project[p]
    project_authors = [a[1] for a in project]
    
    author_to_commits = {}
    author_to_loc = {}
    author_to_invariants = {}

    for tup in project:
        author_to_commits[tup[1]] = int(tup[8])
        author_to_loc[tup[1]] = int(tup[3]) + int(tup[4])
        author_to_invariants[tup[1]] = int(tup[2])

    sorted_author_to_commits = author_to_commits.items()
    sorted_author_to_commits.sort(key=lambda x: x[1])
    
    sorted_author_to_loc = author_to_loc.items()
    sorted_author_to_loc.sort(key=lambda x: x[1])
    
    sorted_author_to_invariants = author_to_invariants.items()
    sorted_author_to_invariants.sort(key=lambda x: x[1])

    author_ranks = {}
    for author in project_authors:
        if author_to_invariants[author] == 0:
            continue

        commit_ranks.append(sorted_author_to_commits.index((author, author_to_commits[author]))/float(len(project_authors)))
        invariant_ranks.append(sorted_author_to_invariants.index((author, author_to_invariants[author]))/float(len(project_authors)))
        loc_ranks.append(sorted_author_to_loc.index((author, author_to_loc[author]))/float(len(project_authors)))

cla()
plot(invariant_ranks, commit_ranks, 'x', markersize=ms/2., alpha=ALPHA)
plot([0, 1], [0, 1], color="#DDDDDD", linewidth=lw*.75)

slope, intercept, r_value, p_value, std_err = stats.linregress(invariant_ranks,commit_ranks)
print slope, intercept, r_value, p_value, std_err, r_value**2

xlabel("Rank %ile (Invariants)")
ylabel("Rank %ile (Commits)")

xlim(xmin=0)
ylim(ymin=0)

savefig('invariant-commit-rank.pdf')


cla()
plot(invariant_ranks, loc_ranks, 'x', markersize=ms/2., alpha=ALPHA)
plot([0, 1], [0, 1], color="#DDDDDD", linewidth=lw*.75)
xlabel("%ile Rank (Invariants)")
ylabel("%ile Rank (LoC)")

xlim(xmin=0)
ylim(ymin=0)

savefig('invariant-loc-rank.pdf')
    
