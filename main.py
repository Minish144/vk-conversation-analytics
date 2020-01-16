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

login = vk_data["login"]
password = vk_data["password"]
access_token = vk_data["access_token"]
owner_id = vk_data["owner_id"]
chat_id = vk_data["chat_id"]
peer_id = 2000000000 + chat_id
session = VkApi(login=login,
                password=password,
                token=access_token)
vk = session.get_api()

def get_messages_total():
    return vk.messages.getHistory(peer_id=peer_id, count=0)['count']

def get_messages():
    for i in range(get_messages_total()//200):
        items = vk.messages.getHistory(peer_id=peer_id, count=200, offset=i*200)['items']
        for k in range(200):
            print(items[k]['text'])



def main():
    print('сообщений всего:', get_messages_total())
    get_messages()

if __name__ == "__main__":
    main()

vk_data_json_file.close()