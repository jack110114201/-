from flask import Flask , request
import json
from model import selectdb

app = Flask(__name__)

@app.route('/')
def index():
    return 'Azure'

#http://localhost:5000/invoice?date={輸入date}
@app.route('/invoice')
def invoice_API():
    invoice = request.args.get('date')
    output =''
    if invoice == None:
        return 'Hi sir ,API使用 /invoice?date={輸入date} ,Thanks'
    else:
        output = selectdb.Mongo_select(int(invoice))
        return json.dumps(output , ensure_ascii=False)
        
if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0' , port=5000)