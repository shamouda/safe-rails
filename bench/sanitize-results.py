
import pickle
from os import system
from glob import glob
from bench_helpers import Result

results = []
for r in glob("../results/*.pkl"):
    results += pickle.load(open(r))

fakeResult = Result(0, 0, 0, "", 0)
    
for r in results:
    for m in r['results']:
        r['results'][m] = [0, [fakeResult]]
    
system("rm -rf ../results/clean; mkdir ../results/clean/ &> /dev/null")

pickle.dump(results, open("../results/clean/clean.pkl", 'w'))
    
