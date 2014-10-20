from finder_helpers import *

projects = []

for proj in listdir('.'):
    if proj == "_scripts":
        continue

    if DO_CHECK_AUTHORS:
        print proj

    switch_hash(proj, "master")
    projects.append(analyze_project(proj))

# number of custom validators
print "TOTAL CUSTOM VALIDATORS", sum([len(p.customs) for p in projects])

# number of builtin validator usages
print  "TOTAL BUILTIN VALIDATORS", sum([sum([len(v) for v in p.builtins.values()]) for p in projects])

# number of builtin association usages
print "TOTAL ASSOCIATIONS", sum([sum([len(v) for v in p.associations.values()]) for p in projects])

# print builtin validators
builtins = defaultdict(lambda: [])
for p in projects:
    for k in p.builtins:
        builtins[k] += p.builtins[k]

builtins_used = builtins.items()
builtins_used.sort(key=lambda i: len(i[1]))
builtins_used.reverse()

for v in builtins_used:                
    print str(len(v[1]))+"\t"+v[0]

# print before callbacks
before_callbacks = defaultdict(lambda: [])
for p in projects:
    for k in p.before_validator_callbacks:
        before_callbacks[k] += p.before_validator_callbacks[k]

before_callbacks_used = before_callbacks.items()
before_callbacks_used.sort(key=lambda i: len(i[1]))
before_callbacks_used.reverse()

print "BEFORE_CALLBACKS:"
for v in before_callbacks_used:                
    print str(len(v[1]))+"\t"+v[0]


# print after callbacks
after_callbacks = defaultdict(lambda: [])
for p in projects:
    for k in p.after_validator_callbacks:
        after_callbacks[k] += p.after_validator_callbacks[k]

after_callbacks_used = after_callbacks.items()
after_callbacks_used.sort(key=lambda i: len(i[1]))
after_callbacks_used.reverse()

print "AFTER_CALLBACKS:"
for v in after_callbacks_used:                
    print str(len(v[1]))+"\t"+v[0]


# print associations
associations = defaultdict(lambda: [])
for p in projects:
    for k in p.associations:
        associations[k] += p.associations[k]

associations_used = associations.items()
associations_used.sort(key=lambda i: len(i[1]))
associations_used.reverse()

print "ASSOCIATIONS:"
for v in associations_used:
    print str(len(v[1]))+"\t"+v[0]

for p in projects:
    if len(p.customs) > 0:
        print p.name
        for c in p.customs:
            print c

for p in projects:
    print "\t".join([str(i) for i in [p.name, sum([len(i) for i in p.builtins.values()]), p.total_lines_measured]])


if DO_CHECK_AUTHORS:
    print "TOTAL AUTHORS :", sum([len(p.authors) for p in projects])
    
    author_scatter = open("_scripts/authors.txt", 'w')
    author_scatter.write("\t".join(["project",
                                    "author",
                                    "invariants_written",
                                    "author_lines_inserted",
                                    "author_lines_deleted",
                                    "total_invariants",
                                    "total_lines_inserted",
                                    "total_lines_deleted",
                                    "author_commits",
                                    "total_commits"])+"\n")
    for p in projects:
        tot_lines_inserted = sum([a[0] for a in p.authors.values()])
        tot_lines_deleted = sum([a[1] for a in p.authors.values()])
        tot_commits = sum([a[2] for a in p.authors.values()])
        tot_blames = sum([i for i in p.authored_invariant.values()])
        if tot_blames == 0:
            continue

        #print p.name, tot_lines
        for a in p.authors:
            author_scatter.write("\t".join([str(i) for i in [p.name, a, p.authored_invariant[a], p.authors[a][0], p.authors[a][1], tot_blames, tot_lines_inserted, tot_lines_deleted, p.authors[a][2], tot_commits]])+"\n")
    author_scatter.close()


if DO_CHECK_LINES:
    proj_stats = open("_scripts/project_stats.txt", 'w')
    proj_stats.write("project, num_authors, num_lines_ruby, num_validations, num_builtin_validations, num_custom_validations, num_associations, num_before_validator_callbacks, num_after_validator_callbacks,num_commits,num_models,num_locks,num_transactions\n")

    for p in projects:
        proj_stats.write(",".join([str(i) for i in [p.name,
                                len(p.authors),
                                p.num_lines_ruby,
                                len(p.customs)+len(p.builtins),
                               len(p.builtins),
                               len(p.customs),
                               len(p.associations),
                               len(p.before_validator_callbacks),
                                                    len(p.after_validator_callbacks),
                                                    p.num_commits,
                                                    p.num_models,
                                                    p.num_locks,
                                                    p.num_transactions]])+"\n")
    proj_stats.close()
