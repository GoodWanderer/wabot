from flask import Flask, request, jsonify
from wabot import WABot
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        print("Тут тип что то будет:\n\n"+bot+"\n\n")
        return bot.processing()

if(__name__) == '__main__':
    app.run()