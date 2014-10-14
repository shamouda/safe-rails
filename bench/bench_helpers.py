
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

    def make_kvp(self, key, value, model="indexed_key_value"):
        self.conn.request("POST",
                    "/"+model+"s",
                          urlencode({model+"[key]":key, model+"[value]":value}),
                    self.headers)
        return self.conn.getresponse()

    def delete_kvp(self, which_key, model="indexed_key_value"):
        self.conn.request("DELETE",
                          "/"+model+"s/"+str(which_key),
                          "",
                          self.headers)
        return self.conn.getresponse()

INSERT = 0

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

def bsp_pool_task(tup):
    rails_host, port, key, value, model = tup
    w = Worker(rails_host+":"+str(port))
    st = datetime.now()
    raw_result = w.make_kvp(key, value, model=model).read()
    et = datetime.now()
    
    lat_ms = (et-st).total_seconds()*1000.

    result = Result(INSERT,
                    key,
                    value,
                    raw_result, lat_ms)

    resultQueue.put(result)
    return 1

def count_duplicates(host, model):
    conn = psycopg2.connect("host=%s dbname=rails user=rails" % (host))
    cur = conn.cursor()
    # YOLO
    cur.execute("SELECT key, COUNT(*) FROM %s GROUP BY key HAVING COUNT(*) > 1;" % (model+"s"))
    return cur.fetchall()
    


def bsp_bench(rails_host, parallelism=100, trials=10, port=3000, model="indexed_key_value"):
    w = Worker(rails_host+":"+str(port))
    response = w.make_kvp("peter", "bar")
    print response.status, response.reason, response.read()
    
    response = w.delete_kvp(1)
    print response.status, response.reason, response.read()

    v = "bar"

    p = Pool(parallelism)

    fails = []
    allresults = []
    for nameit in range(0, trials):
        k = str(nameit)
        workers = [(rails_host, port, k, v, model) for i in range(0, parallelism)]

        p.map(bsp_pool_task, workers)

        results = []
        for i in range(0, parallelism):
            results.append(resultQueue.get())

        f = sum(1 for r in results if r.success)
        print nameit, f, average([r.lat_ms for r in results])

        fails.append(f)
    
    allresults.append(results)
    return fails, results
    



def ssh(host, cmd, user='ubuntu', bg=False):
    cmd = "ssh -o StrictHostKeyChecking=no %s@%s \"%s\" %s" % (user, host, cmd, "&" if bg else "")
    system(cmd)

def reset_postgres(host):
    ssh(host, "killall ssh")
    ssh(host, "~/safe-rails/scripts/reset-pg.sh &> /tmp/pg.out", bg=True)

def start_passenger(host, nprocs):
    ssh(host, "cd ~/safe-rails/demo; passenger stop")
    ssh(host, "cd ~/safe-rails/demo; sudo pkill -9 passenger; passenger start --max-pool-size %d --min-instances %d &> /tmp/passenger.out & disown" % (nprocs, nprocs), bg=True)
