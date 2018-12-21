import requests
import json
import os

token = os.getenv('TELEGRAM_TOKEN')
url = 'https://api.hphk.io/telegram/bot{}/getUpdates'.format(token)

response = json.loads(requests.get(url).text)

url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(token)
chat_id = response['result'][-1]['message']['from']['id'] 
msg = response['result'][-1]['message']['text']

requests.get(url, params ={"chat_id":chat_id, "text":msg})


