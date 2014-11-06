
from os import system

from random import random, randint
from httplib import HTTPConnection
from urllib import urlencode
from multiprocessing import Pool, Queue
from datetime import datetime
import psycopg2

def average(d):
    return sum(d)/float(len(d))

class Worker:
    def __init__(self, rails_host):
        self.conn = HTTPConnection(rails_host)

        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}

    def insert_kvp(self, key, value, model):
        self.conn.request("POST",
                    "/"+model+"s",
                          urlencode({model+"[key]":key, model+"[value]":value}),
                    self.headers)
        return self.conn.getresponse()

    def insert_user(self, dept_id, model):
        self.conn.request("POST",
                          "/"+model+"s",
                          urlencode({model+"["+model.split("_user")[0]+"_department_id]":dept_id}),
                    self.headers)
        return self.conn.getresponse()

    def insert_department(self, which_id, model):
        self.conn.request("POST",
                          "/"+model+"s",
                          urlencode({model+"[id]":which_id}),
                    self.headers)
        return self.conn.getresponse()

    def destroy_user_or_department(self, which_id, model):
        self.conn.request("DELETE",
                          "/"+model+"s/"+str(which_id),
                          "",
                          self.headers)
        return self.conn.getresponse()

    def delete_id(self, which_id, model):
        self.conn.request("DELETE",
                          "/"+model+"s/"+str(which_id),
                          "",
                          self.headers)
        return self.conn.getresponse()

    def delete_kvp(self, key, model):
        self.conn.request("POST",
                          "/"+model+"s/delete_key",
                          urlencode({model+"[key]":key}),
                          self.headers)
        return self.conn.getresponse()

    def destroy_kvp(self, key, model):
        self.conn.request("POST",
                          "/"+model+"s/delete_key",
                          urlencode({model+"[key]":key}),
                          self.headers)
        return self.conn.getresponse()

    def update_kvp(self, key, value, model):
        self.conn.request("POST",
                          "/"+model+"s/update_key",
                          urlencode({model+"[key]":key, model+"[value]":value}),
                          self.headers)
        return self.conn.getresponse()

    def get_kvp(self, key, model):
        self.conn.request("POST",
                          "/"+model+"s/get_key",
                          urlencode({model+"[key]":key}),
                          self.headers)
        return self.conn.getresponse()


INSERT = 888
DELETE = 999

class Result():
    def __init__(self, reqType, key, value, raw_response, lat_ms):
        self.requestType = reqType
        self.key = key
        self.value = value
        self.raw_response = None#raw_response
        self.success = raw_response.find("ERROR") == -1
        self.lat_ms = lat_ms
        

# multiprocessing needs inheritance
resultQueue = Queue()


def count_duplicates(host, model):
    conn = psycopg2.connect("host=%s dbname=rails user=rails" % (host))
    cur = conn.cursor()
    # YOLO
    cur.execute("SELECT key, COUNT(*) FROM %s GROUP BY key HAVING COUNT(*) > 1;" % (model+"s"))
    return cur.fetchall()

def pk_stress_task(tup):
    rails_host, port, key, value, model = tup
    w = Worker(rails_host+":"+str(port))
    st = datetime.now()
    raw_result = w.insert_kvp(key, value, model).read()
    et = datetime.now()
    
    lat_ms = (et-st).total_seconds()*1000.

    result = Result(INSERT,
                    key,
                    value,
                    raw_result, lat_ms)

    resultQueue.put(result)
    return 1

def pk_stress(rails_host, nclients=100, trials=10, port=3000, model="indexed_key_value"):
    p = Pool(nclients)

    #warm up rails
    for i in range(0, nclients):
        w = Worker(rails_host+":"+str(port))
        w.insert_kvp("-1", "dummy", model).read()
        w = Worker(rails_host+":"+str(port))
        w.delete_kvp("-1", model).read()


    while !resultQueue.empty():
        resultQueue.get()        

    fails = []
    allresults = []

    v = "test"

    for nameit in range(0, trials):
        k = str(nameit)
        workers = [(rails_host, port, k, v, model) for i in range(0, nclients)]

        p.map(pk_stress_task, workers)

        results = []
        for i in range(0, nclients):
            results.append(resultQueue.get())

        f = sum(1 for r in results if r.success)
        print nameit, f, average([r.lat_ms for r in results])

        fails.append(f)
    
    p.terminate()
    allresults.append(results)
    return fails, results

    
def fk_stress_task(tup, doLog=True):
    rails_host, port, which_id, optype, dept_no, model = tup
    w = Worker(rails_host+":"+str(port))
    st = datetime.now()
    
    if dept_no:
        if optype == INSERT:
            raw_result = w.insert_user(dept_no, model).read()
        else:
            raw_result = w.destroy_user_or_department(which_id, model).read()
    else:
        if optype == INSERT:
            raw_result = w.insert_department(which_id, model).read()
        else:
            raw_result = w.destroy_user_or_department(which_id, model).read()
    et = datetime.now()
    
    #print raw_result

    lat_ms = (et-st).total_seconds()*1000.

    result = Result(optype,
                    which_id,
                    None,
                    raw_result,
                    lat_ms)

    if doLog:
        resultQueue.put(result)
    return 1

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out



def fk_stress(rails_host, n_clients=100, trials=10, port=3000, model="simple"):
    w = Worker(rails_host+":"+str(port))
    p = Pool(n_clients)

    user_model = model+"_user"
    dept_model = model+"_department"
    
    print "Warming up..."
    for i in range(0, n_clients):
        w = Worker(rails_host+":"+str(port))
        print w.insert_department(-1, model+"_department").read()
        w = Worker(rails_host+":"+str(port))
        w.destroy_user_or_department(-1, model+"_department").read()
    print "... running!"

    while !resultQueue.empty():
        resultQueue.get()    

    fails = []
    allresults = []
    for nameit in range(0, trials):
        k = str(nameit)

        # insert the department on the "ones" association
        fk_stress_task((rails_host, port, k, INSERT, None, dept_model), doLog=False)
        
        # first task is to delete the "ones"
        workers = [(rails_host, port, k, DELETE, None, dept_model)]
        workers += [(rails_host, port, None, INSERT, k, user_model) for i in range(0, n_clients)]

        p.map(fk_stress_task, workers)

        results = []
        for i in range(0, n_clients+1):
            results.append(resultQueue.get())

        f = sum(1 for r in results if r.success and r.requestType == INSERT)
        print nameit, f, average([r.lat_ms for r in results])

        fails.append(f)

    p.terminate()    
    allresults.append(results)
    return fails, results
    
def count_dangling_users(host, model):
    conn = psycopg2.connect("host=%s dbname=rails user=rails" % (host))
    cur = conn.cursor()
    # YOLO*3
    cur.execute("SELECT %s_department_id AS department_id, COUNT(*) FROM %s_users AS U LEFT OUTER JOIN %s_departments AS D ON U.%s_department_id = D.id WHERE D.id IS NULL GROUP BY %s_department_id HAVING COUNT(*) > 0;" % (model, model, model, model, model))
    return cur.fetchall()

cached_zetas = {}

def zeta(N, theta):
    if (N, theta) in cached_zetas:
        return cached_zetas[(N, theta)]
    ans = 0L
    # linkbench and ycsb use 1/pow(i, theta), not gray's suggested pow(1./N, theta)
    # gray's prose suggest this is a typo... choosing linkbench and ycsb implementation
    for i in range(1, N+1):
        ans += 1.0/pow(i+1, theta)
    cached_zetas[(N, theta)] = ans
    return ans

def gen_zipf(N, theta):
    alpha = 1.0/(1-theta)
    zetan = zeta(N, theta)
    zeta2theta = zeta(2, theta)
    eta = (1.0 - pow(2.0/N, 1-theta))/(1.0-zeta2theta/zetan)
    u = random()
    uz = u*zetan
    if uz < 1:
        return 1
    if uz < 1 + pow(0.5, theta):
        return 2
    return int(1 + N*pow(eta*u-eta+1, alpha))

# copying Gray's paper as in YCSB code; precompute samples to avoid runtime overhead
def gen_zipf_samples(num_samples, N, theta):
    return [gen_zipf(N, theta) for i in range(0, num_samples)]

def gen_ycsb(num_samples, total_num_records):
    # YCSB uses a "ZIPFIAN_CONSTANT" of 0.99; becomes theta
    return gen_zipf_samples(num_samples, total_num_records, 0.99)

def gen_linkbench_write(num_samples, total_num_records):
    # write_shape = 0.741
    return gen_zipf_samples(num_samples, total_num_records, 0.741)

def gen_linkbench_update(num_samples, total_num_records):
    # write_shape = 0.606
    return gen_zipf_samples(num_samples, total_num_records, 0.606)

def gen_random(num_samples, total_num_records):
    return [randint(1, total_num_records) for i in range(0, num_samples)]

#linkbench deletes are uniform!
'''
    # Use uniform rather than skewed distribution for deletes, because:
    # a) we don't want to delete the most frequently read nodes
    # b) nodes can only be deleted once
'''

def ssh(host, cmd, user='ubuntu', bg=False):
    cmd = "ssh -o StrictHostKeyChecking=no %s@%s \"%s\" %s" % (user, host, cmd, "&" if bg else "")
    if bg:
        print cmd
    system(cmd)

def reset_postgres(host):
    ssh(host, "killall ssh")
    ssh(host, "~/safe-rails/scripts/reset-pg.sh &> /tmp/pg.out", bg=True)

def start_passenger(host, nprocs):
    ssh(host, "cd ~/safe-rails/demo; passenger stop")
    ssh(host, "cd ~/safe-rails/demo; sudo pkill -9 passenger; passenger start -d --log-file /tmp/phusion-log.out --max-pool-size %d --min-instances %d &> /tmp/passenger.out" % (nprocs, nprocs), bg=True)

def start_unicorn(host, nprocs):
    ssh(host, "sudo /etc/init.d/nginx stop; cd ~/safe-rails/demo; rm /tmp/*.out; passenger stop &> /dev/null; sudo pkill -9 unicorn_rails; pkill -9 unicorn_rails; killall unicorn_rails; sleep 1; git checkout config/unicorn.rb; rm log/*.log; sudo rm -rf /tmp/*; echo \"worker_processes %d\" >> config/unicorn.rb; unicorn_rails -c config/unicorn.rb -D & sudo /etc/init.d/nginx start;" % (nprocs), bg=True)

def pk_workload_task(tup):
    rails_host, port, model, keys = tup
    value = "test"
    for key in keys:
        w = Worker(rails_host+":"+str(port))
        st = datetime.now()
        raw_result = w.insert_kvp(key, value, model).read()
        et = datetime.now()
    
        lat_ms = (et-st).total_seconds()*1000.
        
        result = Result(INSERT,
                        key,
                        value,
                        raw_result, lat_ms)
        
        resultQueue.put(result)

    return 1

def pk_workload(rails_host, workload="uniform", records=100, model="simple_key_value", ops_per_client=100, n_clients=100, port=3000):
    w = Worker(rails_host+":"+str(port))
    p = Pool(n_clients)

    print "Warming up..."

    #warm up rails
    for i in range(0, n_clients):
        w = Worker(rails_host+":"+str(port))
        w.insert_kvp("-1", "dummy", model).read()
        w = Worker(rails_host+":"+str(port))
        w.delete_kvp("-1", model).read()

    while !resultQueue.empty():
        resultQueue.get()

        
    print "... running!"

    results = []

    if workload == "uniform":
        allKeys = gen_random(ops_per_client*n_clients, records)
    elif workload == "ycsb":
        allKeys = gen_ycsb(ops_per_client*n_clients, records)
    elif workload == "linkbench-ins":
        allKeys = gen_linkbench_write(ops_per_client*n_clients, records)
    elif workload == "linkbench-upd":
        allKeys = gen_linkbench_update(ops_per_client*n_clients, records)

    keys_per_worker = chunkIt(allKeys, n_clients)

    workers = map(lambda keys: (rails_host, port, model, keys), keys_per_worker)

    p.map(pk_workload_task, workers)

    for i in range(0, len(allKeys)):
        results.append(resultQueue.get())

    f = sum(1 for r in results if r.success)

    p.terminate()

    print workload, f, average([r.lat_ms for r in results])

    return f, results


def fk_workload_task(tup):
    rails_host, port, model, ops, users_to_depts, num_depts = tup

    chance_user = float(users_to_depts)/(users_to_depts+1)

    user_model = model+"_user"
    dept_model = model+"_department"

    for i in range(0, ops):
        w = Worker(rails_host+":"+str(port))
        st = datetime.now()
        dept_id = randint(1, num_depts)
        if random() < chance_user:
            raw_result = w.insert_user(dept_id, user_model).read()
            optype = INSERT
        else:
            # delete department
            raw_result = w.destroy_user_or_department(dept_id, dept_model).read()
            optype = DELETE

        et = datetime.now()
        lat_ms = (et-st).total_seconds()*1000.
        
        result = Result(optype,
                        dept_id,
                        None,
                        raw_result,
                        lat_ms)
        resultQueue.put(result)

    return 1

def fk_workload(rails_host, workload="uniform", records=100, model="simple", ops_per_client=100, n_clients=100, port=3000, users_to_dept=10):
    w = Worker(rails_host+":"+str(port))
    p = Pool(n_clients)

    print "Warming up..."
    for i in range(0, n_clients):
        w = Worker(rails_host+":"+str(port))
        print w.insert_department(-1, model+"_department").read()
        w = Worker(rails_host+":"+str(port))
        w.destroy_user_or_department(-1, model+"_department").read()
    print "... running!"

    # populate all of the departments
    n_depts = records
    print "populating ", n_depts, "departments"
    for d in range(1, n_depts+1):
        print "populating department", d
        w = Worker(rails_host+":"+str(port))
        w.insert_department(d, model+"_department")
    print "populated!"

    while !resultQueue.empty():
        resultQueue.get()        

    results = []
    workers = [(rails_host, port, model, ops_per_client, users_to_dept, records) for i in range(0, n_clients)]

    p.map(fk_workload_task, workers)

    for i in range(0, n_clients*ops_per_client):
        results.append(resultQueue.get())

    f = sum(1 for r in results if r.success)
    p.terminate()

    print workload, f, average([r.lat_ms for r in results])

    return f, results
