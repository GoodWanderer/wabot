from flask import Flask, request, jsonify
from wabot import WABot, sendmessage
import json

import time
from timeloop import Timeloop
from datetime import timedelta


app = Flask(__name__)

# a = True
# while a:
#     sleep(3)
#     print(1)

tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print("2s job current time : {}".format(time.ctime()))

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        return bot.processing()

if(__name__) == '__main__':
    app.run()