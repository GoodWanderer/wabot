import json
import requests

import datetime
from datetime import datetime
import pytz

import admin
import secret

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
        self.APIUrl = secret.APIUrl
        self.token = secret.token
        self.id = secret.id

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{self.id}/{method}?token={self.token}"
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
            welcome_string = """Для того что бы получить информацию о вебенаре, отправьте:\n "О вебинаре" """

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
                if 'fromMe' in  message:

                    text = message['body']
                    id = message['chatId']

                    result = admin.select_user(id)

                    if result == None or result == []:
                        admin.create_user(id)

                    result = admin.select_user(id)

                    result_post = admin.select_post()

                    if text.lower() == 'о вебинаре':
                        return self.welcome(id)

                    elif text.lower() == '/admin':

                        admin.update_user_flag(id, 1)

                        return self.admin(id)

                    elif result[1] == 1 and text == secret.password:
                        if result_post == [] or result_post == None or  result_post[7] == 0:
                            admin.update_user_flag(id, 2)
                            return self.questionTextPost(id)

                        else:
                            admin.update_user_flag(id, 10)
                            a = str('-'.join((str(result_post[2]), str(result_post[3]),
                                              str(result_post[4]), str(result_post[5]),
                                              str(result_post[6]))))
                            return self.send_message(str(result[0]), str(
                                result_post[1]) + "\n\n" + a + "\n\n" + 'Удалить рассылку? "Удалить"')

                    elif result[1] == 2:
                        if result_post == [] or result_post == None:
                            #Создать с с айди и спросить о времяни
                            admin.update_user_flag(id, 3)
                            admin.create_post(id, text)
                            return self.questionTextTime(id)

                        else:
                            # Изменить
                            admin.update_user_flag(id, 3)
                            admin.update_post(text, id)
                            return self.questionTextTime(id)

                    elif result[1] == 3:
                        admin.update_user_flag(id, 4)
                        admin.update_post_time(text.split('-'), id)

                        return self.info(id, result_post[1], str(text))

                    elif result[1] == 4 and text.lower() == 'да':
                        admin.update_user_flag(id, 0)
                        admin.update_post_flag(id, 1)
                        #Добавить сообщение об успешной отпраки

                    elif result[1] == 10 and text.lower() == 'удалить':
                        admin.update_user_flag(id, 0)
                        admin.update_post_flag(id, 0)
                        return self.send_message(result[0], 'Рассылка отменена')
                    else:
                        return self.welcome(id, True)

                    # if text == 'ку':
                    #     print("\n\n\n"+"Какой-то челик, ля ля ля:"+"\n\n\n")
                    #     cur.execute("SELECT * FROM posts WHERE flag = 1")
                    #     result = cur.fetchone()
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
                    #                 print("\n\n\nКакая-то фигня\n\n\n")

                else:
                    result_post = admin.select_post_flag(1)

                    if result_post != None and result_post != []:

                        if result_post[7] == 1:

                            dt_s = str(result_post[4])+'.'+str(result_post[3])+'.'+str(result_post[2])+' '+str(result_post[5])+':'+str(result_post[6])
                            dt_fmt = '%d.%m.%Y %H:%M'

                            res = datetime.strptime(dt_s, dt_fmt)

                            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
                            print(str(moscow_time))

                            dt_s = str(moscow_time.day)+'.'+str(moscow_time.month)+'.'+str(moscow_time.year)+' '+str(moscow_time.hour)+':'+str(moscow_time.minute)
                            moscow_time = datetime.strptime(dt_s, dt_fmt)
                            print(str(moscow_time.day))

                            if moscow_time >= res:

                                admin.delete_post()
                                results = admin.select_users_all()

                                for result in results:
                                    self.send_message(str(result[0]), str(result_post[1]))

                    return 'NoCommand'