
from bench_helpers import *
from time import sleep
import pickle

PG_HOST = "ec2-54-203-221-73.us-west-2.compute.amazonaws.com"
RAILS_HOST = "ec2-54-245-166-54.us-west-2.compute.amazonaws.com"

use_nginx = True

def reset_hosts(nprocs):
    print "Starting PG"
    reset_postgres(PG_HOST)
    sleep(4)
    print "Starting rails"
    if not use_nginx:
        start_passenger(RAILS_HOST, nprocs)
        sleep(2)
    else:
        start_unicorn(RAILS_HOST, nprocs)
        sleep(10)

print "Starting bench"

pk_models = ["unique_key_value", "indexed_key_value", "simple_key_value"]
fk_models = ["simple", "belongs_to", "dbfk"]

STRESS_RAILS_WORKERS = [1, 2, 4, 8, 16, 32, 64]

BENCH_PK_STRESS = True
BENCH_FK_STRESS = True
BENCH_PK_WORKLOAD = True
BENCH_FK_WORKLOAD = True

STRESS_CLIENTS = 64
STRESS_TRIALS = 100
iterations = 2

FK_USERS_TO_DEPT_PROPORTION = 10

NUMRECORDS_PK = [1, 10, 100, 1000, 10000, 100000]
NUMRECORDS_FK = [1, 10, 100, 1000, 10000, 100000]
OPS_PER_CLIENT = 100
WORKLOADS = ["ycsb", "linkbench-ins", "linkbench-upd", "uniform"]
RECORD_TEST_N_RAILS_PROCS = 64
RECORD_TEST_N_CLIENTS =64

OUTFILE = "/mnt/external/results.pkl"

ALL_RESULTS = []

if BENCH_PK_WORKLOAD:
    for it in range(0, iterations):
        for workload in WORKLOADS:
            for records in NUMRECORDS_PK:
                pk_bench_model_results = {}
                pk_bench_dups = {}
                for m in pk_models:
                    print "STARTING", m, "..."
                    print RECORD_TEST_N_RAILS_PROCS, RECORD_TEST_N_CLIENTS
                    reset_hosts(RECORD_TEST_N_RAILS_PROCS)

                    pk_bench_model_results[m] = pk_workload(RAILS_HOST,
                                                            workload=workload,
                                                            records=records, 
                                                            model=m,
                                                            ops_per_client=OPS_PER_CLIENT,
                                                            n_clients=RECORD_TEST_N_CLIENTS)
                    pk_bench_dups[m] = count_duplicates(PG_HOST, m)
                    print pk_bench_dups
                    ALL_RESULTS.append({ 
                        "bench":"PK_WORKLOAD",
                        "workload":workload,
                        "records":records,
                        "model":m,
                        "ops_per_client":OPS_PER_CLIENT,
                        "iteration":it,
                        "rails_procs":RECORD_TEST_N_RAILS_PROCS,
                        "clients":RECORD_TEST_N_CLIENTS,
                        "results": pk_bench_model_results,
                        "dups" : pk_bench_dups
                    })  
                    pickle.dump(ALL_RESULTS, open(OUTFILE, 'w'))

if BENCH_PK_STRESS:
    for it in range(0, iterations):
        for nprocs in STRESS_RAILS_WORKERS:
            pk_stress_model_results = {}
            pk_stress_dups = {}
            for m in pk_models:
                print "STARTING", m, "..."
                reset_hosts(nprocs)
                pk_stress_model_results[m] = pk_stress(RAILS_HOST, model=m, nclients=STRESS_CLIENTS, trials=STRESS_TRIALS)
                pk_stress_dups[m] = count_duplicates(PG_HOST, m)
                print pk_stress_dups[m]
                ALL_RESULTS.append({ 
                "bench":"PK_STRESS",
                "model":m,
                "iteration":it,
                "rails_procs":nprocs,
                "clients":STRESS_CLIENTS,
                "results": pk_stress_model_results,
                "dups" : pk_stress_dups
                })
                pickle.dump(ALL_RESULTS, open(OUTFILE, 'w'))

if BENCH_FK_WORKLOAD:
    for it in range(0, iterations):
        for workload in ["unused"]:
            for records in NUMRECORDS_FK:
                fk_bench_model_results = {}
                fk_bench_dups = {}
                for m in fk_models:
                    print "STARTING", m, "..."
                    print RECORD_TEST_N_RAILS_PROCS, RECORD_TEST_N_CLIENTS
                    reset_hosts(RECORD_TEST_N_RAILS_PROCS)

                    fk_bench_model_results[m] = fk_workload(RAILS_HOST,
                                                            records=records, 
                                                            model=m,
                                                            ops_per_client=OPS_PER_CLIENT,
                                                            n_clients=RECORD_TEST_N_CLIENTS,
                                                            users_to_dept=FK_USERS_TO_DEPT_PROPORTION)
                    fk_bench_dups[m] = count_dangling_users(PG_HOST, m)
                    print fk_bench_dups
                    ALL_RESULTS.append({ 
                        "bench":"FK_WORKLOAD",
                        "users_to_dept":FK_USERS_TO_DEPT_PROPORTION,
                        "records":records,
                        "model":m,
                        "ops_per_client":OPS_PER_CLIENT,
                        "iteration":it,
                        "rails_procs":RECORD_TEST_N_RAILS_PROCS,
                        "clients":RECORD_TEST_N_CLIENTS,
                        "results": fk_bench_model_results,
                        "dups" : fk_bench_dups
                    })  

                    pickle.dump(ALL_RESULTS, open(OUTFILE, 'w'))

if BENCH_FK_STRESS:
    for it in range(0, iterations):
        for nprocs in STRESS_RAILS_WORKERS:
            fk_stress_model_results = {}
            fk_stress_dups = {}
            for m in fk_models:
                print "STARTING", m, "..."
                reset_hosts(nprocs)
                fk_stress_model_results[m] = fk_stress(RAILS_HOST, model=m, n_clients=STRESS_CLIENTS, trials=STRESS_TRIALS)
                fk_stress_dups[m] = count_dangling_users(PG_HOST, m)
                print fk_stress_dups[m]
                ALL_RESULTS.append({ 
                    "bench":"FK_STRESS",
                    "model":m,
                    "iteration":it,
                    "rails_procs":nprocs,
                    "clients":STRESS_CLIENTS,
                    "results": fk_stress_model_results,
                    "dangling" : fk_stress_dups
            })

            pickle.dump(ALL_RESULTS, open(OUTFILE, 'w'))

exit(0)


