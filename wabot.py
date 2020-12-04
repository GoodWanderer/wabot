import json
import requests

import datetime
from datetime import datetime
import pytz

import admin
import secret

class WABot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.APIUrl = secret.APIUrl
        self.token = secret.token
        self.id = secret.id

    def send_requests(self, chatId, text, method='sendMessage'):
        url = f"{self.APIUrl}{self.id}/{method}?token={self.token}"
        data = {"chatId": chatId, "body": text}
        if method != 'sendMessage':
            data = {"chatId": chatId, "body": secret.img, "filename": 'img.jpg'}
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def welcome(self, chatId, noWelcome=False):
        if (noWelcome == False):
            welcome_string = "Информация о вебинаре\n"
        else:
            welcome_string = """Для того что бы получить информацию о вебенаре, отправьте:\n"О вебинаре" """
        return  self.send_requests(chatId, welcome_string, 'sendFile'), self.send_requests(chatId, welcome_string)

    def admin_text_pas(self, chatId):
        return self.send_requests(chatId, "Введите пароль:")

    def post_text(self, chatId):
        return self.send_requests(chatId, "Введите текст поста:")

    def post_time(self, chatId):
        return self.send_requests(chatId, "Введите, через '-', время рассылки по мск (+3)\n" +
                                          "часы-минуты-день-месяц-год:\n" +
                                          "xx-xx-xx-xx-xxxx")

    def post_check(self, chatId, text, time):
        a = time.split('-')
        return self.send_requests(chatId, text+
                                         '\n\nДата '+str(a[2])+'-'+str(a[3])+'-'+str(a[4])+
                                         '\nВремя '+str(a[0])+' : '+str(a[1])+
                                         '\n\nВсё верно?\nДля подтверждения отправьте: "Да"')

    def post_delete(self, chatId, a):
        return self.send_requests(chatId, str(a[1]) +
                                         '\n\nДата ' + str(a[4]) + '-' + str(a[5]) + '-' + str(a[6]) +
                                         '\nВремя ' + str(a[3]) + ' : ' + str(a[2]) +
                                         '\n\nОтменить рассылку?\nДля отмены отправьте: "Отменить"')

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
                        return self.admin_text_pas(id)

                    elif result[1] == 1 and text == secret.password:
                        if result_post == [] or result_post == None or  result_post[7] == 0:
                            admin.update_user_flag(id, 2)
                            return self.post_text(id)

                        else:
                            admin.update_user_flag(id, 10)
                            return self.post_delete(id, result_post)

                    elif result[1] == 2:
                        if result_post == [] or result_post == None:
                            admin.update_user_flag(id, 3)
                            admin.create_post(id, text)
                            return self.post_time(id)

                        else:
                            admin.update_user_flag(id, 3)
                            admin.update_post(id, text)
                            return self.post_time(id)

                    elif result[1] == 3:
                        admin.update_user_flag(id, 4)
                        admin.update_post_time(id, text.split('-'))

                        return self. post_check(id, result_post[1], str(text))

                    elif result[1] == 4 and text.lower() == 'да':
                        admin.update_user_flag(id, 0)
                        admin.update_post_flag(id, 1)
                        return self.send_requests(id, 'Рассылка успешно назначенна')

                    elif result[1] == 10 and text.lower() == 'отменить':
                        admin.update_user_flag(id, 0)
                        admin.update_post_flag(id, 0)
                        return self.send_requests(id, 'Рассылка отменена')
                    else:
                        return self.welcome(id, True)

                else:
                    result_post = admin.select_post_flag(1)

                    if result_post != None and result_post != []:

                        if result_post[7] == 1:

                            dt_s = str(result_post[4])+'.'+str(result_post[5])+'.'+str(result_post[6])+' '+str(result_post[3])+':'+str(result_post[2])
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
                                    self.send_requests(str(result[0]), str(result_post[1]))

                    return 'NoCommand'