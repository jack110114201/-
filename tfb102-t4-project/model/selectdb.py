import pymongo
# import urllib.parse
from sshtunnel import SSHTunnelForwarder
    
server = SSHTunnelForwarder(('3.113.29.214', 22), #連線AWS遠端主機
    ssh_password='koxhAS?ZRayMorAddS6*HzZMZ3LFh*wK',
    ssh_username='Administrator',
    remote_bind_address=('127.0.0.1', 27017))

def Mongo_start(): #主機啟動
    server.start()
    client=pymongo.MongoClient('127.0.0.1', server.local_bind_port)
    # username = urllib.parse.quote_plus('root')
    # password = urllib.parse.quote_plus('123456')
    # client = pymongo.MongoClient(f'mongodb://{username}:{password}@db:27017/')
    return client

def Mongo_select(date):
    while True:
        try:
            client = Mongo_start()
            mydb = client.Azure
            collection = mydb.invoice
            json_data = collection.find_one({'Date':date} , {'_id':0})
            client.close()
            server.stop()
            break
        except:
            server.stop()
            pass
    return json_data

def Mongo_db_add(data): #把Azure加入至資料
    while True:
        try:
            client = Mongo_start()
            mydb = client.Azure
            collection = mydb.invoice
            # collection.drop()
            collection.insert(data)
            client.close()
            print('OK!')
            server.stop()
            break
        except:
            server.stop()
            pass

def Mongo_db_select(): #查詢最後中獎發票的月份
    while True:
        try:
            client = Mongo_start()
            mydb = client.Azure
            collection = mydb.invoice
            if collection.find_one() != None:
                result = collection.aggregate([{'$group':
                {"_id":"$item" , 'maxDate':{'$max':"$Date"}}
                }])
                client.close()
                start_Date =''
                for i in result:
                    start_Date = str(i['maxDate'])
            else :
                client.close()
                start_Date  = None
            server.stop()
            break
        except:
            server.stop()
            pass
    return start_Date
