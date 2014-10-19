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

"git log --author="Alex Watt" --pretty=tformat: --numstat"

for proj in listdir('.'):
    if proj == "_scripts":
        continue
    
    ruby_files = find_files(proj, "*.rb")
    for f in ruby_files:
        
