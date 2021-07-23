import requests
import json
from model import selectdb

date = '11003'
# url = f'http://localhost:5000/invoice?date={date}'

# res = requests.get(url=url)
# json_data = json.loads(res.text)

# print(type(json_data))
# print(json_data['頭獎'])

print(selectdb.Mongo_select(11003))
