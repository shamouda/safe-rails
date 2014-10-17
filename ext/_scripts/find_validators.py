from os import listdir, system, walk, path
import fnmatch, itertools
from collections import defaultdict

def find_files(directory, pattern):
    for root, dirs, files in walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = path.join(root, basename)
                if True:#filename.find("/test/") == -1:
                    yield filename

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
        
    projectStat = ProjectStats(proj)
    projects.append(projectStat)
    totlines = 0

    
    ruby_files = find_files(proj, "*.rb")
    for f in ruby_files:
        all_lines = open(f).read().split('\n')
        lineno = 0
        line = ""
        while lineno < len(all_lines):
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
                name = line.split()[1]
                projectStat.customs[name].append(CustomValidator(f, lineno, line))
            if line.find("before_validation") != -1:
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
            line = ""
            
    projectStat.total_lines = totlines

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
    print "\t".join([str(i) for i in [p.name, sum([len(i) for i in p.builtins.values()]), p.total_lines]])
