from os import listdir, system

for d in listdir('.'):
    if d == "_scripts":
        continue
    system("cd "+d+"; echo '"+d+"'; git rev-parse HEAD; git show -s --format=%ci HEAD")
