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

for proj in listdir('.'):
    if proj == "_scripts":
        continue

    system("cd "+proj+"; git checkout master; git pull")
 
