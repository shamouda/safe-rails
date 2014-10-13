
from config import *

from httplib import HTTPConnection
from urllib import urlencode
from multiprocessing import Pool

class Worker:
    def __init__(self):
        self.conn = HTTPConnection(host)

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

w = Worker()
response = w.make_kvp("peter", "bar")
print response.status, response.reason, response.read()

response = w.delete_kvp(1)
print response.status, response.reason, response.read()


age = "bar"

def pool_task(tup):
    name, age = tup
    w = Worker()
    return w.make_kvp(name, age).read()

p = Pool(parallelism)

for nameit in range(0, trials):
    curname = str(nameit)
    workers = [(curname, age) for i in range(0, parallelism)]
    print sum(map(lambda x: 0 if x.find("ERROR") == -1 else 1, p.map(pool_task, workers)))
