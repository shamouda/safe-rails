
from os import system, walk, listdir, path


def find_files(directory, pattern):
    for root, dirs, files in walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = path.join(root, basename)
                if True:#filename.find("/test/") == -1:
                    yield filename

def get_subscribers(user, repo, proj):
    system("curl -i 'https://api.github.com/repos/%s/%s/subscribers' 2>&1 > _scripts/github-stats/%s-subscribers.txt" % (user, repo, proj))

def get_stars(user, repo, proj):
    system("curl -i 'https://api.github.com/repos/%s/%s/stargazers' 2>&1 > _scripts/github-stats/%s-stars.txt" % (user, repo, proj))
                    
for proj in listdir('.'):
    if proj == "_scripts":
        continue

    print proj
    system("cd "+proj+"; git remote -v > /tmp/remote.txt")
    user, repo = open("/tmp/remote.txt").read().split('\n')[0].strip(" (fetch)").split("/")[-2:]
    #print get_subscribers(user, repo, proj)
    print get_stars(user, repo, proj)



