import sqlite3

# 連結至資料庫 game.db
connect = sqlite3.connect('log.db')

# 建立cursor, 以利後續操作
cursor = connect.cursor()

# 建立資料表
cursor.execute("CREATE TABLE log \
               (id integer primary key, \
                name varchar(20), \
                user_id text,\
                invoice_number text,\
                invoice_date text,\
                type text,\
                other text)")
connect.commit()