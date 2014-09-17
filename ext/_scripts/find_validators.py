from os import listdir, system, walk, path
import fnmatch, itertools
from collections import defaultdict

def find_files(directory, pattern):
    for root, dirs, files in walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = path.join(root, basename)
                yield filename

class ProjectStats:
    def __init__(self, name):
        self.name = name
        self.customs = defaultdict(lambda: [])
        self.builtins = defaultdict(lambda: [])

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

projects = []

for proj in listdir('.'):
    if proj == "_scripts":
        continue
        
    projectStat = ProjectStats(proj)
    projects.append(projectStat)
    totlines = 0

    ruby_files = find_files(proj, "*.rb")
    for f in ruby_files:
        lineno = 0
        for line in open(f):
            line = line.strip()
            if len(line) > 0 and line[0] == "#":
                continue
            if line.find("ActiveModel::Validator") != -1:
                name = line.split()[1]
                projectStat.customs[name].append(CustomValidator(f, lineno, line))
            elif line.find("validates") != -1:
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
            lineno += 1
            totlines +=1

    projectStat.total_lines = totlines

# number of custom validators
print sum([len(p.customs) for p in projects])

# number of builtin validator usages
print sum([sum([len(v) for v in p.builtins.values()]) for p in projects])

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


for p in projects:
    if len(p.customs) > 0:
        print p.name
        for c in p.customs:
            print c

for p in projects:
    print "\t".join([str(i) for i in [p.name, sum([len(i) for i in p.builtins.values()]), p.total_lines]])
