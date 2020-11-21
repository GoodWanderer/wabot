from flask import Flask, request, jsonify
from wabot import WABot
import json

from time import sleep

app = Flask(__name__)

# a = True
# while a:
#     sleep(3)
#     print(1)

@app.route('/', methods=['POST'])
def home():
    print(1)
    if request.method == 'POST':
        bot = WABot(request.json)
        return bot.processing()

if(__name__) == '__main__':
    app.run(port=80)