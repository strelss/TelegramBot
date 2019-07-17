from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import re

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot876924589:AAHlQgHAKJFknBQh_bney4Kd1a_dWPRIhRk/'

def send_message(chat_id, text):
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(URL + 'sendMessage', json=answer)
    return r.json()

def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto

def get_prise(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker{}'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]["price_usd"]
    return price

@app.route('/', methods=['POST'])
def index():
    r = request.get_json()
    chat_id = r["message"]["chat"]["id"]
    message = r["message"]["text"]
    pattern = r'/\w+'
    if re.search(pattern, message):
        price = get_prise(parse_text(message))
        send_message(chat_id, text=price)
        return jsonify(r)
    return '<h1>Hello bot!</h1>'

if __name__=='__main__':
    app.run()