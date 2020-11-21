import json
import requests

import datetime
from time import sleep

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
                minute INT,
                flag INT
            )""")

day = 20
month = 11
year = 2020

while True:
    offset = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(offset)
    sleep(5)
    if result == 1 and int(now.year) >= year and int(now.month) >= month and int(now.mi) >= day:
        #Сделать резуль 0
        #цикл фор(который пройдётся по всем и сделать расслку)
        print(now)
        break

print('end')

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

    def questionTextPost(self, chatId):
        welcome_string = "Введите текст поста:\n"
        return self.send_message(chatId, welcome_string)

    def questionTextTime(self, chatId):
        welcome_string = "Введите, через пробел, время рассылки по мск(+3):\nгод-месяц-день-часы-минуты\nxxxx-xx-xx-xx-xx"
        return self.send_message(chatId, welcome_string)

    def info(self, chatId, text, time):
        a = time.split('-')
        welcome_string = text+'\n\nДата: ' + str(a[0])+ ' ' + str(a[1])+ ' ' + str(a[2]) + "\n" + 'Время: ' + str(a[3]) + ' : ' + \
                         str(a[4]+'\n\nВсё верно?("да")')
        return self.send_message(chatId, welcome_string)

    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body']

                if not message['fromMe']:
                    id = message['chatId']

                    #1
                    con = sqlite3.connect('users_db.sqlite')
                    cur = con.cursor()

                    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    result = cur.fetchone()

                    if result == None or result == []:
                        cur.execute("INSERT INTO users values (?, 0)", (int(id),))
                        con.commit()

                    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    result = cur.fetchone()

                    #2
                    cur.execute("SELECT * FROM posts")
                    resultpost = cur.fetchone()


                    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    result = cur.fetchone()

                    if text.lower() == 'хотел бы узнать о вебинаре':
                        con.close()

                        return self.welcome(id)

                    elif text.lower() == '/admin':

                        cur.execute("""UPDATE users SET flag = 1 WHERE id = ?""", (id,))
                        con.commit()
                        con.close()

                        return self.admin(id)

                    elif text == 'Jero2012' and result[1] == 1:
                        cur.execute("""UPDATE users SET flag = 2 WHERE id = ?""", (id, ))
                        con.commit()
                        con.close()
                        return self.questionTextPost(id)

                    elif result[1] == 2:
                        if resultpost == [] or resultpost == None:
                            #Создать с с айди и спросить о времяни
                            cur.execute("""UPDATE users SET flag = 3 WHERE id = ?""", (id,))
                            con.commit()
                            cur.execute("INSERT INTO posts values (?, ?, 0, 0, 0, 0, 0, 0)", (id, text))
                            con.commit()
                            return self.questionTextTime(id)

                        elif resultpost[7] == 1:
                            #Вывести результат и сделать id 0
                            cur.execute("""UPDATE users SET flag = 0 WHERE id = ?""", (id,))
                            con.commit()
                            a = str('-'.join((str(resultpost[2]), str(resultpost[3]),
                                                                              str(resultpost[4]), str(resultpost[5]),
                                                                              str(resultpost[6]))))
                            return self.info(id, resultpost[1], a)
                        else:
                            # Изменить
                            cur.execute("""UPDATE posts SET sendText = ? WHERE id = ?""", (text, id))
                            con.commit()
                            cur.execute("""UPDATE users SET flag = 3 WHERE id = ?""", (id,))
                            con.commit()
                            return self.questionTextTime(id)

                    elif result[1] == 3:
                        a = text.split('-')
                        cur.execute("""UPDATE users SET flag = 4 WHERE id = ?""", (id,))
                        con.commit()
                        cur.execute("""UPDATE posts SET year=?, month=?, day=?, hour=?, minute=? WHERE id = ?""",
                                    (int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), id))
                        con.commit()
                        return self.info(id, resultpost[1], str(text))

                    elif result[1] == 4 and text.lower() == 'да':
                        cur.execute("""UPDATE users SET flag = 0 WHERE id = ?""", (id,))
                        con.commit()
                        cur.execute("""UPDATE posts SET flag=1 WHERE id = ?""", (id,))
                        con.commit()
                    else:
                        con.close()
                        return self.welcome(id, True)
                else:
                    return 'NoCommand'