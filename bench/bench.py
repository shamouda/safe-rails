
from bench_helpers import *
from time import sleep

PG_HOST = "ec2-54-203-221-73.us-west-2.compute.amazonaws.com"
RAILS_HOST = "ec2-54-203-221-73.us-west-2.compute.amazonaws.com"

def reset_hosts(nprocs):
    print "Starting PG"
    reset_postgres(PG_HOST)
    sleep(5)
    print "Starting rails"
    start_passenger(RAILS_HOST, nprocs)
    sleep(2)

print "Starting bench"

models = ["indexed_key_value", "simple_key_value", "unique_key_value"]

model_results = {}
dups = {}

nprocs = 10

for m in models:
    print "STARTING"
    print m
    print "...",

    reset_hosts(nprocs)
    model_results[m] = bsp_bench(RAILS_HOST, model=m, parallelism=10, trials=100)
    dups[m] = count_duplicates(RAILS_HOST, m)
    print dups[m]

exit(0)


