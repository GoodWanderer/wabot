import json
import requests
import datetime

class WABot():
    def __init__(self, json):
        self.json = json
        print('\n\n'+"тест"+'\n\n')
        self.dict_messages = json['data']
        self.APIUrl = 'https://api-whatsapp.io/api/ceae53d7-8c29-4a80-a6f9-8a548f303a83'
        self.token = 'vfgs0ezuk4tcqxs709zis3uv677omv09mkxorwkhax='

    def send_requests(self, method, data):
        print("send_requests")
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatId, text):
        print('\n\n'+chatId+'\n\n')
        data = {"chatId": chatId,
                "body": text}

        answer = self.send_requests('sendMessage', data)
        return answer

    def welcome(self, chatId, noWelcome=False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "WhatsApp Demo Bot Python\n"
            print('\n\nwelcome\n\n')
        else:
            welcome_string = """Incorrect command
        Commands:
        1. chatId - show ID of the current chat
        2. time - show server time
        3. me - show your nickname
        4. file [format] - get a file. Available formats: doc/gif/jpg/png/pdf/mp3/mp4
        5. ptt - get a voice message
        6. geo - get a location
        7. group - create a group with the bot"""

        return self.send_message(chatId, welcome_string)

    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body'].split()
                if not message['fromMe']:
                    id = message['chatId']
                    if text[0].lower() == 'hi':
                        print("\n\nНу хоть проверка есть))\n\n")
                        return self.welcome(id)
                    elif text[0].lower() == 'time':
                        return self.time(id)
                    elif text[0].lower() == 'chatId':
                        return self.show_chat_id(id)
                    elif text[0].lower() == 'me':
                        return self.me(id, message['senderName'])
                    elif text[0].lower() == 'file':
                        return self.file(id, text[1])
                    elif text[0].lower() == 'ptt':
                        return self.ptt(id)
                    elif text[0].lower() == 'geo':
                        return self.geo(id)
                    elif text[0].lower() == 'group':
                        return self.group(message['author'])
                    else:
                        return self.welcome(id, True)
                else:
                    return 'NoCommand'