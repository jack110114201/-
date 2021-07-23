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

db = client.UIN
print(db)
collection = db.UIN

award_period = {"_id":"11-12-2020"}
number = "39993297"

for prize in collection.find(award_period):
    print(prize)

    if prize["Special Prize"] == number:
        print("恭喜中一千萬")
        break
    elif prize["Grand Prize"] == number:
        print("恭喜中二百萬")
        break
    else:
        for x in prize["First Prize"]:
            if x == number:
                print("恭喜中二十萬",x)
            else:
                pass