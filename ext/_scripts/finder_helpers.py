from os import listdir, system, walk, path
import fnmatch, itertools
from collections import defaultdict


DO_CHECK_AUTHORS = True
DO_CHECK_LINES = True

def is_association(l):
    filters = ["belongs_to", "has_one", "has_many", "has_and_belongs_to"]
    for f in filters:
        if l.find(f) != -1 and l.split()[0] != "def":
            return True
    return False

def find_files(directory, pattern):
    for root, dirs, files in walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = path.join(root, basename)
                if filename.find("/spec/") == -1 and filename.find("/test/") == -1 and filename.find("vendor/plugins") == -1 and filename.find("vendor/rails") == -1:
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

def get_githashes(project_dir, resetMaster=False):
    if not DO_CHECK_LINES:
        return {}

    if resetMaster:
        system("cd "+project_dir+"; git checkout master")
    
    system("cd "+project_dir+"; git log --oneline > /tmp/hashes.txt")
    return [line.split(' ')[0] for line in open("/tmp/hashes.txt").read().split('\n')]

def get_lastcommit_date(project_dir):
    system("cd "+project_dir+"; git log -1 --format=%cd . > /tmp/date.txt")

    return open("/tmp/date.txt").read().strip()

def switch_hash(project_dir, which):
    system("cd "+project_dir+"; git checkout "+which)
    #if which == "master":
    #    system("cd "+project_dir+"; git pull")

def blame_line(project, f, line):
    if not DO_CHECK_AUTHORS:
        return None

    # git blame line numbers are indexed from 1, we are indexed by 0
    system("cd "+project+"; git blame -c -L %d,%d %s > /tmp/blame.txt" % (line+1, line+1, f.split("/", 1)[-1]))
    ret = open("/tmp/blame.txt").read().split('\t')[1][1:]
    return ret.strip()

def nild(d):
    return num_items_lists_in_dict(d)

def num_items_lists_in_dict(d):
    return sum([len(l) for l in d.values()])
        
                    
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

def analyze_project(proj):
    projectStat = ProjectStats(proj)
    totlines = 0

    projectStat.num_lines_ruby = numlines_rails(proj)
    projectStat.authors = get_authors(proj)
    projectStat.authored_invariant = defaultdict(int)
    projectStat.num_commits = len(get_githashes(proj))
    projectStat.last_commit_date = get_lastcommit_date(proj)

    projectStat.num_models = 0
    projectStat.num_transactions = 0
    projectStat.num_locks = 0
    projectStat.num_validations = 0

    ruby_files = find_files(proj, "*.rb")
    for f in ruby_files:
        try:
            all_lines = open(f).read().split('\n')
        except IOError as e:
            print "Error opening file "+f, e, "skipping!"
            continue

        lineno = 0
        line = ""
        while lineno < len(all_lines):
            blame = False
            validations_this_line = 0
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

            if ((line.replace(" ", "").find("<ActiveRecord::Base") != -1 or
                 line.replace(" ","").find("<Spree::Base") != -1 or
                 line.replace(" ","").find("<Refinery::Core::BaseModel") != -1)
                and line.find("class") != -1):
                projectStat.num_models += 1
            
            if line.find(".lock.") != -1 or line.find(".lock!") != -1:
                projectStat.num_locks += 1

            if line.find(".transaction do") != -1:
                projectStat.num_transactions += 1

            if line.find("ActiveModel::Validator") != -1:
                blame = True
                name = line.split()[1]
                validations_this_line += 1                
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
                        validations_this_line += 1                
                        s = True
                    if line.find(":inclusion") != -1 or line.find("inclusion:") != -1:
                        projectStat.builtins["validates_inclusion"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1
                        s = True
                    if line.find(":numericality") != -1 or line.find("numericality:") != -1:
                        projectStat.builtins["validates_numericality"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True
                    if line.find(":date") != -1 or line.find("date:") != -1:
                        projectStat.builtins["validates_date"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True
                    if line.find(":file_size") != -1 or line.find("file_size:") != -1:
                        projectStat.builtins["vaildates_file_size"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True
                    if line.find(":format") != -1 or line.find("format:") != -1:
                        projectStat.builtins["validates_format"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True
                    if line.find(":uniqueness") != -1 or line.find("uniqueness:") != -1:
                        projectStat.builtins["validates_uniqueness"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True
                    if line.find(":length") != -1 or line.find("length:") != -1:
                        projectStat.builtins["validates_length"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True                        
                    if line.find(":email") != -1 or line.find("email:") != -1:
                        projectStat.builtins["validates_email"].append(BuiltInValidator(f, lineno, line))
                        validations_this_line += 1                        
                        s = True
                    if ((line.find('it "validates') != -1 and line.find(" do") != -1) or
                        ((line.find("it '") != -1 or line.find('it "') != -1) and line.find(" do") != -1)):
                        validations_this_line += 1                        
                        projectStat.builtins['unknown'].append(BuiltInValidator(f, lineno, line))
                        print "Extra", line
                        s = True
                    if not s:
                        print f, lineno, line
                                         
                else:
                    validations_this_line += 1                    
                    projectStat.builtins[name].append(BuiltInValidator(f, lineno, line))
            if blame:
                projectStat.authored_invariant[blame_line(proj, f, lineno)] += validations_this_line

            projectStat.num_validations += validations_this_line
            lineno += 1
            totlines +=1
            line = ""

    projectStat.total_lines_measured = totlines
    return projectStat
