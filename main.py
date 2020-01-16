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

class vk_class:
    login = vk_data["login"]
    password = vk_data["password"]
    access_token = vk_data["access_token"]
    owner_id = vk_data["owner_id"]
    chat_id = vk_data["chat_id"]
    session = VkApi(login=login,
                    password=password,
                    token=access_token)

def main():
    vk = vk_class.session.get_api()
    vk.messages.send(chat_id = vk_class.chat_id, message='test', random_id = random.random())

if __name__ == "__main__":
    main()

vk_data_json_file.close()