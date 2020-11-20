import json
import requests
import datetime

import sqlite3

con = sqlite3.connect('users_db.sqlite')

cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INT,
                flag INT
            )""")

cur2 = con.cursor()
cur2.execute("""CREATE TABLE IF NOT EXISTS posts(
                id INT,                
                sendText TEXT,
                year INT,
                month INT,
                day INT,
                hour INT,
                minute INT
            )""")

class WABot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.APIUrl = 'https://api-whatsapp.io/api/'
        self.token = 'vfgs0ezuk4tcqxs709zis3uv677omv09mkxorwkhax='
        self.id = 'ceae53d7-8c29-4a80-a6f9-8a548f303a83/'

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{self.id}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        print("send_requests")
        return answer.json()

    def send_message(self, chatId, text):
        data = {"chatId": chatId,
                "body": text}

        answer = self.send_requests('sendMessage', data)
        return answer

    def welcome(self, chatId, noWelcome=False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "Информация о вебинаре\n"
        else:
            welcome_string = """Для того что бы получить информацию о вебенаре, отправьте:\n "Хотел бы узнать о вебинаре" """

        return self.send_message(chatId, welcome_string)

    def admin(self, chatId):
        welcome_string = "Введите пароль\n"
        return self.send_message(chatId, welcome_string)

    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body']

                if not message['fromMe']:
                    id = message['chatId']

                    con = sqlite3.connect('users_db.sqlite')
                    cur = con.cursor()

                    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    result = cur.fetchone()

                    print(str(id))
                    print("\n\n"+"gg: "+str(result)+"\n\n")

                    if result == None or result == []:
                        cur.execute("INSERT INTO users values (?, 0)", (int(id),))
                        con.commit()
                        print(1)

                    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    result = cur.fetchone()
                    print("\n\n"+'res= '+str(result)+"\n\n")

                    if text.lower() == 'хотел бы узнать о вебинаре':
                        return self.welcome(id)

                    elif text.lower() == '/admin':

                        cur.execute("""UPDATE users SET flag = 1 WHERE id = ?""", (id,))
                        con.commit()
                        con.close()

                        return self.admin(id)
                    # elif text[0].lower() == 'chatId':
                    #     return self.show_chat_id(id)
                    # elif text[0].lower() == 'me':
                    #     return self.me(id, message['senderName'])
                    # elif text[0].lower() == 'file':
                    #     return self.file(id, text[1])
                    # elif text[0].lower() == 'ptt':
                    #     return self.ptt(id)
                    # elif text[0].lower() == 'geo':
                    #     return self.geo(id)
                    # elif text[0].lower() == 'group':
                    #     return self.group(message['author'])

                    elif text == 'Jero2012' and result[1] == 1:
                        print('\n\nПароль\n\n')
                        return self.welcome(id)
                    else:
                        return self.welcome(id, True)
                else:
                    return 'NoCommand'