
from bench_helpers import *
from time import sleep
import pickle

PG_HOST = "ec2-54-203-221-73.us-west-2.compute.amazonaws.com"
RAILS_HOST = "ec2-54-203-221-73.us-west-2.compute.amazonaws.com"

def reset_hosts(nprocs):
    print "Starting PG"
    reset_postgres(PG_HOST)
    sleep(4)
    print "Starting rails"
    start_passenger(RAILS_HOST, nprocs)
    sleep(2)

print "Starting bench"

pk_models = ["indexed_key_value", "simple_key_value", "unique_key_value"]
fk_models = ["simple", "belongs_to", "dbfk"]

NPROCS = [1, 2, 4, 8, 16, 32, 64]

BENCH_PK_STRESS = True
BENCH_FK_STRESS = True

iterations = 2

FK_USERS_TO_DEPT_PROPORTION = 10

OUTFILE = "results.pkl"

ALL_RESULTS = []

if BENCH_PK_STRESS:
    for it in range(0, iterations):
        for nprocs in NPROCS:
            pk_stress_model_results = {}
            pk_stress_dups = {}
            for m in pk_models:
                print "STARTING", m, "..."
                reset_hosts(nprocs)
                pk_stress_model_results[m] = pk_stress(RAILS_HOST, model=m, parallelism=64, trials=10)
                pk_stress_dups[m] = count_duplicates(PG_HOST, m)
                print pk_stress_dups[m]
                ALL_RESULTS.append({ 
                "bench":"PK_STRESS",
                "model":m,
                "iteration":it,
                "rails_procs":nprocs,
                "results": pk_stress_model_results,
                "dups" : pk_stress_dups
                })


if BENCH_FK_STRESS:
    for it in range(0, iterations):
        for nprocs in NPROCS:
            fk_stress_model_results = {}
            fk_stress_dups = {}
            for m in fk_models:
                print "STARTING", m, "..."
                reset_hosts(nprocs)
                fk_stress_model_results[m] = fk_stress(RAILS_HOST, model=m, parallelism=64, trials=10)
                fk_stress_dups[m] = count_dangling_users(PG_HOST, m)
                print fk_stress_dups[m]
                ALL_RESULTS.append({ 
                    "bench":"FK_STRESS",
                    "model":m,
                    "iteration":it,
                    "rails_procs":nprocs,
                    "results": fk_stress_model_results,
                    "dangling" : fk_stress_dups
            })

pickle.dump(ALL_RESULTS, open(OUTFILE, 'w'))

exit(0)


