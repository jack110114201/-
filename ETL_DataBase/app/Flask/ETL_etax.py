import requests
from bs4 import BeautifulSoup
from datetime import datetime
from model import selectdb

if selectdb.Mongo_db_select() != None :
    start_Date = selectdb.Mongo_db_select()
    start_Date_y = int(start_Date[:3])
    start_Date_m = int(start_Date[3:])+2
else:
    start_Date_y = 101
    start_Date_m = 1

end_Date_y = int(str(datetime.today())[:4]) - 1911
Mongo_data = []
for y in range(start_Date_y , end_Date_y+1 , 1 ):
    for m in range(start_Date_m,12,2):
        if m < 10:
            ym = str(y)+'0'+str(m)
        else:
            ym = str(y)+str(m)
        url = f'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_{ym}/'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
        res = requests.get(url=url , headers=headers)
        if res.status_code == requests.codes.ok :
            res.encoding = "utf-8"  #處理網站編碼不同
            soup = BeautifulSoup(res.text , 'html.parser')
            table = soup.select('table.table.table-bordered')[0]
            table_tr=table.select('tr')
            invoice_num = {'Date':int(ym)}
            for i in [1,3,5,-2]:
                num = table_tr[i].select('td')[0].text.replace('、',' ').strip().split(' ')
                invoice_num[table_tr[i].select('th')[0].text] = num
            # print(invoice_num)
            Mongo_data.append(invoice_num)
    start_Date_m = 1 #重製月份

print(Mongo_data)
if len(Mongo_data) > 0 : #判斷list是否有東西
    selectdb.Mongo_db_add(Mongo_data)





