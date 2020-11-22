from flask import Flask, request, jsonify
from wabot import WABot, sendmessage
import json

import time
import threading

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        return bot.processing()

def sheduler(n):
  _time = time.time()
  print('start loop', n)
  while True:
    if _time + 1 < time.time():
      print(n, ':', time.time())
      sendmessage()
      _time = time.time()

    time.sleep(10)

th1 = threading.Thread(target=app.run)
th2 = threading.Thread(target=sheduler, args=(2,))

th1.start()
th2.start()

# if(__name__) == '__main__':
#     app.run()