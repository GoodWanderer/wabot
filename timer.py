import json
import requests
from time import sleep

APIUrl = 'https://api-whatsapp.io/api/'
token = 'mjhcu14sbf1ui0w1706bsxqpq191mnridkcwk7iti='

id = '5d621b50-d8bf-49c6-9606-df8a6e9fd466'

while True:
    sleep(60)
    url = f"{APIUrl}{id}/{'sendMessage'}?token={token}"
    data = {"chatId": '79608581942', "body": 'q'}
    headers = {'Content-type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)
