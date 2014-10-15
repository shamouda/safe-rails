
from os import system

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

    def insert_kvp(self, key, value, model="indexed_key_value"):
        self.conn.request("POST",
                    "/"+model+"s",
                          urlencode({model+"[key]":key, model+"[value]":value}),
                    self.headers)
        return self.conn.getresponse()

    def insert_user(self, dept_id, model="simple_user"):
        self.conn.request("POST",
                          "/"+model+"s",
                          urlencode({model+"["+model.split("_user")[0]+"_department_id]":dept_id}),
                    self.headers)
        return self.conn.getresponse()

    def insert_department(self, which_id, model="simple_user"):
        self.conn.request("POST",
                          "/"+model+"s",
                          urlencode({model+"[id]":which_id}),
                    self.headers)
        return self.conn.getresponse()

    def destroy_user_or_department(self, which_id, model="simple_user"):
        self.conn.request("DELETE",
                          "/"+model+"s/"+str(which_id),
                          "",
                          self.headers)
        return self.conn.getresponse()

    def delete_id(self, which_id, model="indexed_key_value"):
        self.conn.request("DELETE",
                          "/"+model+"s/"+str(which_id),
                          "",
                          self.headers)
        return self.conn.getresponse()

    def delete_kvp(self, key, model="indexed_key_value"):
        self.conn.request("POST",
                          "/"+model+"s/delete_key",
                          urlencode({model+"[key]":key}),
                          self.headers)
        return self.conn.getresponse()

    def destroy_kvp(self, key, model="indexed_key_value"):
        self.conn.request("POST",
                          "/"+model+"s/delete_key",
                          urlencode({model+"[key]":key}),
                          self.headers)
        return self.conn.getresponse()

    def update_kvp(self, key, value, model="indexed_key_value"):
        self.conn.request("POST",
                          "/"+model+"s/update_key",
                          urlencode({model+"[key]":key, model+"[value]":value}),
                          self.headers)
        return self.conn.getresponse()

    def get_kvp(self, key, model="indexed_key_value"):
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
        self.raw_response = raw_response
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
    raw_result = w.insert_kvp(key, value, model=model).read()
    et = datetime.now()
    
    lat_ms = (et-st).total_seconds()*1000.

    result = Result(INSERT,
                    key,
                    value,
                    raw_result, lat_ms)

    resultQueue.put(result)
    return 1

def pk_stress(rails_host, parallelism=100, trials=10, port=3000, model="indexed_key_value"):
    w = Worker(rails_host+":"+str(port))
    p = Pool(parallelism)

    fails = []
    allresults = []

    v = "test"

    for nameit in range(0, trials):
        k = str(nameit)
        workers = [(rails_host, port, k, v, model) for i in range(0, parallelism)]

        p.map(pk_stress_task, workers)

        results = []
        for i in range(0, parallelism):
            results.append(resultQueue.get())

        f = sum(1 for r in results if r.success)
        print nameit, f, average([r.lat_ms for r in results])

        fails.append(f)
    
    allresults.append(results)
    return fails, results

    
def fk_stress_task(tup, doLog=True):
    rails_host, port, which_id, optype, dept_no, model = tup
    w = Worker(rails_host+":"+str(port))
    st = datetime.now()
    
    if dept_no:
        if optype == INSERT:
            raw_result = w.insert_user(dept_no, model=model).read()
        else:
            raw_result = w.destroy_user_or_department(which_id, model=model).read()
    else:
        if optype == INSERT:
            raw_result = w.insert_department(which_id, model=model).read()
        else:
            raw_result = w.destroy_user_or_department(which_id, model=model).read()
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

def fk_stress(rails_host, parallelism=100, trials=10, port=3000, model="simple"):
    w = Worker(rails_host+":"+str(port))
    p = Pool(parallelism)

    user_model = model+"_user"
    dept_model = model+"_department"
    
    fails = []
    allresults = []
    for nameit in range(0, trials):
        k = str(nameit)

        # insert the department on the "ones" association
        fk_stress_task((rails_host, port, k, INSERT, None, dept_model), doLog=False)
        
        # first task is to delete the "ones"
        workers = [(rails_host, port, k, DELETE, None, dept_model)]
        workers += [(rails_host, port, None, INSERT, k, user_model) for i in range(0, parallelism)]

        p.map(fk_stress_task, workers)

        results = []
        for i in range(0, parallelism+1):
            results.append(resultQueue.get())

        f = sum(1 for r in results if r.success and r.requestType == INSERT)
        print nameit, f, average([r.lat_ms for r in results])

        fails.append(f)
    
    allresults.append(results)
    return fails, results
    
def count_dangling_users(host, model):
    conn = psycopg2.connect("host=%s dbname=rails user=rails" % (host))
    cur = conn.cursor()
    # YOLO*3
    cur.execute("SELECT %s_department_id AS department_id, COUNT(*) FROM %s_users AS U LEFT OUTER JOIN %s_departments AS D ON U.%s_department_id = D.id WHERE D.id IS NULL GROUP BY %s_department_id HAVING COUNT(*) > 0;" % (model, model, model, model, model))
    return cur.fetchall()

def zeta(N, theta):
    ans = 0L
    # linkbench and ycsb use 1/pow(i, theta), not gray's suggested pow(1./N, theta)
    # gray's prose suggest this is a typo... choosing linkbench and ycsb implementation
    for i in range(1, N+1):
        ans += 1.0/pow(i+1, theta)
    return ans

def gen_zipf(N, theta):
    alpha = 1.0/(1-theta)
    zetan = zeta(N, theta)
    eta = (1.0 - pow(2.0/n, 1-theta))/(1.0-zeta(theta, 2)/zetan)
    u = random()
    uz = u*zetan
    if uz < 1:
        return 1
    if uz < 1 + pow(0.5, theta):
        return 2
    return 1 + n*pow(eta*u-eta+1, alpha)

# copying Gray's paper as in YCSB paper; precompute samples to avoid runtime overhead
def gen_zipf_samples(num_samples, N, theta):
    return [gen_zipf(N, theta) for i in range(0, num-samples)]

def gen_ycsb(num_samples, total_num_records):
    # YCSB uses a "ZIPFIAN_CONSTANT" of 0.99; becomes theta
    return gen_zipf_samples(num_samples, total_num_records, 0.99)

def gen_linkbench_write(num_samples, total_num_records):
    # write_shape = 0.741
    return gen_zipf_samples(num_samples, total_num_records, 0.741)

def gen_linkbench_update(num_samples, total_num_records):
    # write_shape = 0.606
    return gen_zipf_samples(num_samples, total_num_records, 0.606)

#linkbench deletes are uniform!
'''
    # Use uniform rather than skewed distribution for deletes, because:
    # a) we don't want to delete the most frequently read nodes
    # b) nodes can only be deleted once
'''

def ssh(host, cmd, user='ubuntu', bg=False):
    cmd = "ssh -o StrictHostKeyChecking=no %s@%s \"%s\" %s" % (user, host, cmd, "&" if bg else "")
    system(cmd)

def reset_postgres(host):
    ssh(host, "killall ssh")
    ssh(host, "~/safe-rails/scripts/reset-pg.sh &> /tmp/pg.out", bg=True)

def start_passenger(host, nprocs):
    ssh(host, "cd ~/safe-rails/demo; passenger stop")
    ssh(host, "cd ~/safe-rails/demo; sudo pkill -9 passenger; passenger start -d --log-file /tmp/phusion-log.out --max-pool-size %d --min-instances %d &> /tmp/passenger.out & disown" % (nprocs, nprocs), bg=True)
