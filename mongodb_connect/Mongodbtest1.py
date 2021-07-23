from pymongo import MongoClient
import atexit
from sshtunnel import SSHTunnelForwarder
server = SSHTunnelForwarder(('3.113.29.214', 22),
    ssh_password='koxhAS?ZRayMorAddS6*HzZMZ3LFh*wK',
    ssh_username='Administrator',
    remote_bind_address=('127.0.0.1', 27017))
server.start()

def shutdown():
    server.stop()

atexit.register(shutdown)

client = MongoClient('127.0.0.1', server.local_bind_port)

db = client.test
print(db)
collection = db.test

for result in collection.find():
    print(result)

collection.insert_one({"x":"1","y":"2"
    })
collection.insert_one({
    "z":"1",
    "a":"2"
    })

# collection.drop()