
from os import system, walk, listdir, path

stars = {}
subscribers = {}

for f in listdir('github-stats'):
    f = "github-stats/"+f
    proj = f.split("-")[1].split("/")[1]
    if f.find("stars.txt") != -1:
        p_stars = open(f).read().count("    \"login\":")
        stars[proj] = p_stars
    elif f.find("subscribers.txt") != -1:
        p_subscribers = open(f).read().count("    \"login\":")
        subscribers[proj] = p_subscribers

for p in stars:
    print p, stars[p], subscribers[p]
