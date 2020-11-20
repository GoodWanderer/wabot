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
                minute INT,
                flag INT
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

    def questionTextPost(self, chatId):
        welcome_string = "Введите текст поста:\n"
        return self.send_message(chatId, welcome_string)

    def questionTextTime(self, chatId):
        welcome_string = "Введите, через пробел, время рассылки по мск(+3):\nгод-месяц-день-часы-минуты\nxxxx-xx-xx-xx-xx"
        return self.send_message(chatId, welcome_string)

    def info(self, chatId, text, time):
        welcome_string = str(text) + " - " + str(time)
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
                    print("\n\n"+'res= '+str(result)+"\n\n")

                    #2
                    cur.execute("SELECT * FROM posts")
                    resultpost = cur.fetchone()


                    cur.execute("SELECT * FROM users WHERE id=?", (int(id),))
                    result = cur.fetchone()
                    print("\n\n" + 'res= ' + str(result) + "\n\n")

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
                        print("\n\nХоть пошло\n\n")
                        if resultpost == [] or resultpost == None:
                            #Создать с с айди и спросить о времяни
                            print("\n\n" + '1' + "\n\n")
                            cur.execute("""UPDATE users SET flag = 3 WHERE id = ?""", (id,))
                            con.commit()
                            cur.execute("INSERT INTO posts values (?, ?, 0, 0, 0, 0, 0, 0)", (id, text))
                            con.commit()
                            return self.questionTextTime(id)

                        elif resultpost[0][7] == 1:
                            #Вывести результат и сделать id 0
                            print("\n\n"+'2'+"\n\n")
                            cur.execute("""UPDATE users SET flag = 0 WHERE id = ?""", (id,))
                            con.commit()
                            return self.questionTextTime(id)
                        else:
                            # Изменить
                            print("\n\n" + '3' + "\n\n")
                            cur.execute("""UPDATE posts SET sendText = ? WHERE id = ?""", (text, id))
                            con.commit()
                            cur.execute("""UPDATE users SET flag = 0 WHERE id = ?""", (id,))
                            con.commit()
                            return self.questionTextTime(id)

                    elif result[1] == 3:
                        a = text.split('-')
                        print(text)
                        cur.execute("""UPDATE posts SET year=?, month=?, day=?, hour=?, minute=? WHERE id = ?""", (a[0], a[1], a[2], a[3], a[4], id))
                        con.commit()
                        return self.info(id, str(resultpost[0][1]), 'gg')

                    else:
                        con.close()
                        return self.welcome(id, True)
                else:
                    return 'NoCommand'