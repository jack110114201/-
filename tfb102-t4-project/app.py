from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from model import formrecognizer_by_url,receipt,selectdb
import tempfile, os
from imgurpython import ImgurClient
from config import *
import datetime 
# import for database
import sqlite3

app = Flask(__name__)

# LINE BOT info
line_bot_api = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'image', 'tmp')

# connect to database
connect = sqlite3.connect('log.db',check_same_thread=False)
cursor = connect.cursor()

@app.route("/callback", methods=['POST'])
def callback():
    # signature:LINE官方提供用來檢查該訊息是否透過LINE官方APP傳送
    signature = request.headers['X-Line-Signature']
    # 用戶傳送的訊息，並且是以JSON的格式傳送
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    # 接收訊息
    message_type = event.message.type
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    
    if isinstance(event.message, ImageMessage):

        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='jpg' + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        #上傳圖片   
        
        dist_path = tempfile_path + '.jpg'
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(Client_ID, Client_secret, access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'invoice'
            }
            path = os.path.join('image', 'tmp', dist_name)
            images = client.upload_from_path(path, config=config, anon=False)
            print(images)
            image_url = images['link']

            number_id = formrecognizer_by_url.formrecognizer_by_url(image_url) 
            invoice_date = number_id['日期']       
            invoice_number = number_id['發票號碼']  

            D = datetime.datetime.today().strftime('%m%d')
            today = int(D)
            date_x = int(str(int(invoice_date)+2)[3:] + str('25')) 
            if today > date_x :
                receipt_data = selectdb.Mongo_select(int(invoice_date))
                ans = receipt.receipt_mechine([invoice_number],receipt_data)
                # 回傳訊息的方法
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans[0][2]))
                # save into database
                cursor.execute("INSERT INTO log (name, user_id, invoice_number, invoice_date, type, other) \
                                VALUES (?, ?, ?, ?, ?, ?)", (user_name, user_id, invoice_number, invoice_date,message_type,image_url))
                connect.commit()
            else: 
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='未開獎'))
                # save into database
                cursor.execute("INSERT INTO log (name, user_id, invoice_number, invoice_date, type, other) \
                                VALUES (?, ?, ?, ?, ?, ?)", (user_name, user_id, invoice_number, invoice_date,message_type,'未開獎'))
                connect.commit()
            return 0


        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
                
            # save into database
            cursor.execute("INSERT INTO log (name, user_id, invoice_number, invoice_date, type, other) \
                            VALUES (?, ?, ?, ?, ?, ?)", (user_name, user_id, None, None,message_type,'上傳失敗'))
            connect.commit()
            return 0
        
    elif isinstance(event.message, TextMessage):
        message = event.message.text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = message))
        # save into database
        cursor.execute("INSERT INTO log (name, user_id, invoice_number, invoice_date, type, other) \
                        VALUES (?, ?, ?, ?, ?, ?)", (user_name, user_id, None, None,message_type,message))
        connect.commit()
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "Error"))
        # save into database
        cursor.execute("INSERT INTO log (name, user_id, invoice_number, invoice_date, type, other) \
                        VALUES (?, ?, ?, ?, ?, ?)", (user_name, user_id, None, None,message_type,message_type))
        connect.commit()
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

