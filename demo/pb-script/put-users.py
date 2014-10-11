
from config import *

from httplib import HTTPConnection
from urllib import urlencode
from multiprocessing import Pool

class Worker:
    def __init__(self):
        self.conn = HTTPConnection(host)

        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}

    def make_user(self, name, age):
        self.conn.request("POST",
                    "/users",
                    urlencode({"user[name]":name, "user[age]":str(age)}),
                    self.headers)
        return self.conn.getresponse()

    def delete_user(self, which_id):
        self.conn.request("DELETE",
                          "/users/"+str(which_id),
                          "",
                          self.headers)
        return self.conn.getresponse()

w = Worker()
response = w.make_user("peter", 4)
print response.status, response.reason, response.read()

response = w.delete_user(51)
print response.status, response.reason, response.read()


age = 23

def pool_task(tup):
    name, age = tup
    w = Worker()
    return w.make_user(name, age).read()

p = Pool(parallelism)

for nameit in range(0, trials):
    curname = str(nameit)
    workers = [(curname, age) for i in range(0, parallelism)]
    print sum(map(lambda x: 0 if x.find("ERROR") == -1 else 1, p.map(pool_task, workers)))
