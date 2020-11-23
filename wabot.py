import json
import requests

import datetime
from time import sleep

from datetime import datetime
import pytz

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

# def sendmessage():
#     print("\n\n\n"+"Старт выполнения"+"\n\n\n")
#     cur.execute("SELECT * FROM posts WHERE flag = 1")
#     result = cur.fetchone()
#     print("Результат: "+str(result))
#     if result != None or result != []:
#         if result[7] == 1:
#             offset = datetime.timezone(datetime.timedelta(hours=3))
#             now = datetime.datetime.now(offset)
#             if result == 1 and int(now.year) >= result[2] and int(now.month) >= result[3] and int(now.day) >= result[4] and int(now.day) >= result[5] and int(now.minuten) >= result[6]:
#                 print("\n\n\nПринт\n\n\n")
#                 cur.execute("""DELETE posts WHERE flag = 1""")
#                 con.commit()
#                 con.close()
#             else:
#                 print("\n\n\nВсё норм, сработает позже\n\n\n")


class WABot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.APIUrl = 'https://api-whatsapp.io/api/'
        self.token = 'vfgs0ezuk4tcqxs709zis3uv677omv09mkxorwkhax='
        self.id = '1d02f38d-3731-47a2-931d-f46a59db273c/'

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
                print("\n\n"+str(message)+"\n\n")
                if 'fromMe' in  message:
                    text = message['body']
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
                        return self.welcome(id)

                    elif text.lower() == '/admin':

                        cur.execute("""UPDATE users SET flag = 1 WHERE id = ?""", (id,))
                        con.commit()

                        return self.admin(id)

                    elif text == 'Jero2012' and result[1] == 1:
                        cur.execute("""UPDATE users SET flag = 2 WHERE id = ?""", (id, ))
                        con.commit()
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
                        return self.welcome(id, True)

                    if text == 'ку':
                        print("\n\n\n"+"Какой-то челик, ля ля ля:"+"\n\n\n")
                        cur.execute("SELECT * FROM posts WHERE flag = 1")
                        result = cur.fetchone()
                        if result != None or result != []:
                            if result[7] == 1:
                                offset = datetime.timezone(datetime.timedelta(hours=3))
                                now = datetime.datetime.now(offset)
                                if result == 1 and int(now.year) >= result[2] and int(now.month) >= result[3] and int(now.day) >= result[4] and int(now.day) >= result[5] and int(now.minuten) >= result[6]:
                                    print("\n\n\nПринт\n\n\n")
                                    cur.execute("""DELETE posts WHERE flag = 1""")
                                    con.commit()
                                    con.close()
                                else:
                                    print("\n\n\nКакая-то фигня\n\n\n")

                else:
                    print("\n\nТест\n\n")
                    con = sqlite3.connect('users_db.sqlite')
                    cur = con.cursor()

                    #2
                    cur.execute("SELECT * FROM posts WHERE flag = 1")
                    resultpost = cur.fetchone()
                    print("\n\n"+str(resultpost)+"\n\n")
                    if resultpost != None or resultpost != []:
                        if resultpost[7] == 1:
                            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
                            if moscow_time.year == resultpost[2] and moscow_time.month == resultpost[3] and moscow_time.day == resultpost[4]:
                                if moscow_time.hour == resultpost[5] and moscow_time.minute == resultpost[6]:
                                    print("\n\nЭммм\n\n")
                                    cur.execute("SELECT * FROM users")
                                    results = cur.fetchall()

                                    for result in results:
                                        self.send_message(str(result[0]), str(resultpost[1]))

                    # cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    # result = cur.fetchone()
                    # APIUrl = 'https://api-whatsapp.io/api/'
                    # token = 'vfgs0ezuk4tcqxs709zis3uv677omv09mkxorwkhax='
                    # id = '1d02f38d-3731-47a2-931d-f46a59db273c/'
                    # method = 'sendMessage'
                    # data = {"chatId": '79608581942',
                    #         "body": 'Ку'}
                    # headers = {'Content-type': 'application/json'}
                    #
                    # url = f"{APIUrl}{id}{method}?token={token}"
                    #
                    # requests.post(url, data=json.dumps(data), headers=headers)
                    return 'NoCommand'