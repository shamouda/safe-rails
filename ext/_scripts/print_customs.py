
NCONTEXT = 25

def get_lines(f, start, nlines):
    return '\n'.join(open(f).read().split('\n')[start-1:start-1+nlines])

for line in open('custom-validations.txt'):
    sline = line.split()
    fname, lineno = sline[-1].split(":")
    lineno = int(lineno)
    print
    print line.strip()
    print get_lines("../"+fname, lineno, NCONTEXT)
    print
    
