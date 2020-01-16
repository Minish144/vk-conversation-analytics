import requests
import string
import json
from vk_api import VkApi
from vk_api import VkUpload
import time
from datetime import timezone
from datetime import datetime
import os
import urllib.request
import random

with open("vk_data.json", "r") as vk_data_json_file:
        vk_data = json.load(vk_data_json_file)

# # # # # # # # # # # # # # # # # # # # # # #
                                            #
login = vk_data["login"]                    #
password = vk_data["password"]              #
access_token = vk_data["access_token"]      #
owner_id = vk_data["owner_id"]              #
chat_id = vk_data["chat_id"]                #       Авторизация ВК
peer_id = 2000000000 + chat_id              #       с помощью данных, 
session = VkApi(login=login,                #       запиханных в json
                password=password,          #
                token=access_token)         #
vk = session.get_api()                      #
                                            #
# # # # # # # # # # # # # # # # # # # # # # #

def get_messages_total():
    return vk.messages.getHistory(peer_id=peer_id, count=0)['count']

def get_messages(messages, messages_amount_per_week, messages_amount_total):
    time_current = time.time()
    time_week_ago = time_current-604800
    #for i in range(messages_amount_total//200):
    for i in range(5):
        items = vk.messages.getHistory(peer_id=peer_id, count=200, offset=i*200)['items']
        for k in range(200):
            print(items[k]['text'])
            messages += items[k]['text'] + ' '
        messages_amount_per_week += k
        if items[k]['date'] <= time_week_ago:
            break
    print(messages, '\n', messages_amount_per_week)

def main():
    messages_amount_total = get_messages_total()
    messages_amount_per_week = 0
    messages = ''
    get_messages(messages, messages_amount_per_week, messages_amount_total)
    print('сообщения:', messages)
    print('сообщений в конфе за 7 дней:', messages_amount_per_week)

    
if __name__ == "__main__":
    main()

vk_data_json_file.close()