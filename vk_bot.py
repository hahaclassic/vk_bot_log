# -*- coding: utf-8 -*- 

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import datetime
import random


token = "55a412a9757a2cbe766ea91e3aa1adb90c8ec9d715ee668ec854af5a62431f5dd7b3d6979b24789c151f6"

vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

login_count = 0

print("VK BOT LOGGER V0.1 IS ACTIVE")

def get_login(login):
    result = requests.get('https://us-central1-test-8b242.cloudfunctions.net/cl?login={}&password=MIIEowIBAAKCAQEA3FapfU0FQgIINq8xMJd'.format(login))
    if result.json()["Status"] == 1:
        return True
    else:
        return False

def delete_login(login):
    requests.get('https://us-central1-test-8b242.cloudfunctions.net/dl?login={}&password=MIIEowIBAAKCAQEA3FapfU0FQgIINq8xMJd'.format(login))
    return True

def send_message(id, message):
        vk.messages.send(
            user_id=id,
            random_id=random.randint(0, 999999),
            message='[{}]: {}'.format(datetime.datetime.now(), message)
        )

def getCommand(text):
    txt = str(text).split()

    if len(txt) >= 2:

        try:
            
            command = txt[0].lower()
            win_id = txt[1]

            return command, win_id

        except Exception as e:
            send_message(260777926, "Команда не распознана, попробуй ещё раз. Ошибка: {}".format(e))
    else:
        send_message(260777926, "Команда не распознана, попробуй ещё раз.")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.from_user:

            if event.user_id == 260777926:

                command, login, = getCommand(text=event.text)
                
                if command == "+":
                    if get_login(login):
                        send_message(260777926, "Логин {} успешно создан.".format(login))
                        login_count += 1
                        send_message(262971013, "Создан логин: {}. Логинов с момента запуска: {}".format(login, login_count))
                    else:
                        send_message(260777926, "Ошибка: логин {} уже занят. Попробуй другой.".format(login))
                        send_message(262971013, "Попытка создания логина: {}. Логин уже занят.".format(login))
                elif command == "-" :
                    if delete_login(login):
                        send_message(260777926, "Логин {} успешно удален.".format(login))
                        send_message(262971013, "Логин {} был удален.".format(login))
                else:
                    send_message(260777926, "Команда не распознана, попробуй ещё раз.")
