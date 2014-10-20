from finder_helpers import *
from collections import defaultdict

projects = []

max_hashes_per_proj = 100

outfile = open("_scripts/historical.txt", 'w')

outfile.write(",".join(["name",
                       "commit_no",
                       "num_commits",
                       "githash",
                       "num_authors",
                       "num_lines_ruby",
                       "num_validations",
                       "num_builtin_validations",
                       "num_custom_validations",
                       "num_associations",
                       "num_before_validator_callbacks",
                       "num_after_validator_callbacks",
                        "num_models",
                        "num_locks",
                        "num_transactions"])+"\n")

for proj in listdir('.'):
    if proj == "_scripts":
        continue

    hashes = get_githashes(proj)
    if len(hashes) > max_hashes_per_proj:
        spacing = int(len(hashes)/float(max_hashes_per_proj))
        print len(hashes), spacing, spacing*max_hashes_per_proj
        to_check = [i*spacing for i in range(0, max_hashes_per_proj)]
        if to_check[-1] == len(hashes):
            to_check[-1] = len(hashes)-1
        else:
            to_check += [len(hashes)-1]
    else:
        to_check = range(0, len(hashes))

    cnt = 0
    for i in to_check:
        cnt += 1
        print "%s %d/%d (commit number %d)" % (proj, cnt, len(to_check), i)
        githash = hashes[i]
        switch_hash(proj, githash)
        p = analyze_project(proj)
        outfile.write(",".join([str(i) for i in [p.name,
                               i,
                               len(hashes),
                               githash,                               
                               len(p.authors),
                               str(p.num_lines_ruby),
                               len(p.customs)+len(p.builtins),
                               len(p.builtins),
                               len(p.customs),
                               len(p.associations),
                               len(p.before_validator_callbacks),
                               len(p.after_validator_callbacks),
                                                 p.num_models,
                                                 p.num_locks,
                                                 p.num_transactions]])+"\n")
        outfile.flush
