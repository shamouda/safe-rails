from os import listdir, system, walk, path
import fnmatch, itertools
from collections import defaultdict

DO_CHECK_AUTHORS = True
DO_CHECK_LINES = True

def find_files(directory, pattern):
    for root, dirs, files in walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = path.join(root, basename)
                if True:#filename.find("/test/") == -1:
                    yield filename

def numlines_rails(project_dir):
    if not DO_CHECK_LINES:
        return 0
    system("cd "+project_dir+"; cloc . > /tmp/cloc.txt")
    for line in open("/tmp/cloc.txt"):
        if line[:4] == "Ruby":
            line = line.split()
            return int(line[4])
                    
def get_authors(project_dir):
    if not DO_CHECK_AUTHORS:
        return {}
    
    system("cd "+project_dir+"; git log --format='%aN' | sort -u > /tmp/authors.txt")
    authors = [line.strip() for line in open("/tmp/authors.txt").read().split('\n')[:-1]]
    ret = {}
    for author in authors:
        insertions = 0
        deletions = 0
        commits = 0
        system("cd "+project_dir+"; git log --author=\""+author+"\" --numstat > /tmp/contrib.txt")
        for line in open("/tmp/contrib.txt"):
            line = line.strip()
            if line[:6] == "commit":
                commits += 1
            elif len(line.split("\t")) == 3:
                if line[-3:] == ".rb":
                    line = line.split()
                    if line[0] != "-":
                        insertions += int(line[0])
                    if line[1] != "-":
                        deletions += int(line[1])
        ret[author] = (insertions, deletions, commits)
    return ret

def blame_line(project, f, line):
    if not DO_CHECK_AUTHORS:
        return None

    # git blame line numbers are indexed from 1, we are indexed by 0
    system("cd "+project+"; git blame -c -L %d,%d %s > /tmp/blame.txt" % (line+1, line+1, f.split("/", 1)[-1]))
    return open("/tmp/blame.txt").read().split('\t')[1][1:].replace(",", "cmma")
                    
class ProjectStats:
    def __init__(self, name):
        self.name = name
        self.customs = defaultdict(list)
        self.builtins = defaultdict(list)
        self.associations = defaultdict(list)
        self.before_validator_callbacks = defaultdict(list)
        self.after_validator_callbacks = defaultdict(list)

class CustomValidator:
    def __init__(self, fileName, lineNo, line):
        self.fileName = fileName
        self.lineNo = lineNo
        self.line = line

class BuiltInValidator:
    def __init__(self, fileName, lineNo, line):
        self.fileName = fileName
        self.lineNo = lineNo
        self.line = line

class Association:
    def __init__(self, fileName, lineNo, line):
        self.fileName = fileName
        self.lineNo = lineNo
        self.line = line

class ValidatorCallback:
    def __init__(self, fileName, lineNo, line):
        self.fileName = fileName
        self.lineNo = lineNo
        self.line = line

        
projects = []

def is_association(l):
    filters = ["belongs_to", "has_one", "has_many", "has_and_belongs_to"]
    for f in filters:
        if l.find(f) != -1 and line.split()[0] != "def":
            return True
    return False


for proj in listdir('.'):
    if proj == "_scripts":
        continue

    if DO_CHECK_AUTHORS:
        print proj
        
    projectStat = ProjectStats(proj)
    projects.append(projectStat)
    totlines = 0

    projectStat.num_lines_ruby = numlines_rails(proj)
    projectStat.authors = get_authors(proj)
    projectStat.authored_invariant = defaultdict(int)

    ruby_files = find_files(proj, "*.rb")
    for f in ruby_files:
        all_lines = open(f).read().split('\n')
        lineno = 0
        line = ""
        while lineno < len(all_lines):
            blame = False
            curline = all_lines[lineno].strip()
            
            if len(curline) == 0 or (len(curline) > 0 and curline[0] == "#"):
                lineno += 1
                totlines +=1
                continue

            line += curline
                        
            if curline[-1] == ",":
                lineno += 1
                totlines +=1
                continue
            
            if line.find("ActiveModel::Validator") != -1:
                blame = True
                name = line.split()[1]
                projectStat.customs[name].append(CustomValidator(f, lineno, line))
            if line.find("before_validation") != -1:
                blame = True
                ls = line.split()
                if len(ls) > 1:
                    name = line.split()[1]
                else:
                    name = line
                projectStat.before_validator_callbacks[name].append(ValidatorCallback(f, lineno, line))
            if line.find("after_validation") != -1:
                ls = line.split()

                if len(ls) > 1:
                    name = line.split()[1]
                else:
                    name = line
                projectStat.after_validator_callbacks[name].append(ValidatorCallback(f, lineno, line))
            if is_association(line):
                ls = line.split()
                name = ls[0]
                if name.find(".") != -1:
                    name = name.split(".")[1]
                projectStat.associations[name].append(Association(f, lineno, line))
            if line.find("validates") != -1:
                blame = True
                name = "validates"+line.split('validates')[1].split(' ')[0].split("(:")[0].split("')")[0].split("(")[0].split("+.")[0].split(",")[0].split("/")[0].split('_#')[0].split('\"')[0].split('.')[0].split(":")[0].split("'")[0].split("?")[0].split("+")[0].split("[")[0].split("=")[0]
                if name == "validates":
                    s = False
                    if line.find(":presence") != -1 or line.find("presence:") != -1:
                        projectStat.builtins["validates_presence"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":inclusion") != -1 or line.find("inclusion:") != -1:
                        projectStat.builtins["validates_inclusion"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":numericality") != -1 or line.find("numericality:") != -1:
                        projectStat.builtins["validates_numericality"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":date") != -1 or line.find("date:") != -1:
                        projectStat.builtins["validates_date"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":file_size") != -1 or line.find("file_size:") != -1:
                        projectStat.builtins["vaildates_file_size"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":format") != -1 or line.find("format:") != -1:
                        projectStat.builtins["validates_format"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":uniqueness") != -1 or line.find("uniqueness:") != -1:
                        projectStat.builtins["validates_uniqueness"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if line.find(":length") != -1 or line.find("length:") != -1:
                        projectStat.builtins["validates_length"].append(BuiltInValidator(f, lineno, line))
                        s = True                        
                    if line.find(":email") != -1 or line.find("email:") != -1:
                        projectStat.builtins["validates_email"].append(BuiltInValidator(f, lineno, line))
                        s = True
                    if ((line.find('it "validates') != -1 and line.find(" do") != -1) or
                        ((line.find("it '") != -1 or line.find('it "') != -1) and line.find(" do") != -1)):
                        s = True
                    if not s:
                        print f, lineno, line
                                         
                else:
                    projectStat.builtins[name].append(BuiltInValidator(f, lineno, line))
            if blame:
                projectStat.authored_invariant[blame_line(proj, f, lineno)] += 1

            lineno += 1
            totlines +=1
            line = ""


    projectStat.total_lines_measured = totlines

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
    author_scatter.write("project, author, invariants_written, author_lines_inserted, author_lines_deleted, total_invariants, total_lines_inserted, total_lines_deleted, author_commits, total_commits\n")
    for p in projects:
        tot_lines_inserted = sum([a[0] for a in p.authors.values()])
        tot_lines_deleted = sum([a[1] for a in p.authors.values()])
        tot_commits = sum([a[2] for a in p.authors.values()])
        tot_blames = sum([i for i in p.authored_invariant.values()])
        if tot_blames == 0:
            continue

        #print p.name, tot_lines
        for a in p.authors:
            author_scatter.write("%s, %s, %d, %d, %d, %d, %d, %d, %d, %d\n" % (p.name, a, p.authored_invariant[a], p.authors[a][0], p.authors[a][1], tot_blames, tot_lines_inserted, tot_lines_deleted, p.authors[a][2], tot_commits))
    author_scatter.close()


if DO_CHECK_LINES:
    proj_stats = open("_scripts/project_stats.txt", 'w')
    proj_stats.write("project, num_authors, num_lines_ruby, num_validations, num_builtin_validations, num_custom_validations, num_associations, num_before_validator_callbacks, num_after_validator_callbacks\n")

    for p in projects:
        proj_stats.write(",".join([str(i) for i in [p.name,
                                len(p.authors),
                                p.num_lines_ruby,
                                len(p.customs)+len(p.builtins),
                               len(p.builtins),
                               len(p.customs),
                               len(p.associations),
                               len(p.before_validator_callbacks),
                               len(p.after_validator_callbacks)]])+"\n")
    proj_stats.close()
