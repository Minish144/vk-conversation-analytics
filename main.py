import requests
import json
from vk_api import VkApi
from vk_api import VkUpload
import time
import random
import re
from pymystem3 import Mystem

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

def get_messages_and_count(messages, messages_amount_per_week, messages_amount_total):
    time_current = time.time()
    time_week_ago = time_current-604800
    #for i in range(messages_amount_total//200):
    for i in range(5):
        items = vk.messages.getHistory(peer_id=peer_id, count=200, offset=i*200)['items']
        for k in range(200):
            messages[0] += items[k]['text'] + ' '
        messages_amount_per_week[0] += k
        if items[k]['date'] <= time_week_ago:
            break
    print(messages[0], '\n', messages_amount_per_week[0])

def lemmatize(messages):
    m = Mystem()
    lemmas = m.lemmatize(messages)
    return ''.join(lemmas)

def message_format_and_split(messages):
    s = messages
    reg = re.compile('[^a-zA-Zа-яА-Я ]')
    reg = reg.sub('', s)
    return reg.split()
    
def remove_empty_element(word_list):
    for x in word_list:
        if x == '':
            word_list.remove('')

def main():
    messages_amount_total = get_messages_total()
    messages_amount_per_week = [0]
    messages = ['']
    get_messages_and_count(messages, messages_amount_per_week, messages_amount_total)
    messages = messages[0]; messages_amount_per_week = messages_amount_per_week[0]
    print('сообщений в конфе за 7 дней:', messages_amount_per_week)
    #vk.messages.send(peer_id=peer_id, message=f'Сообщений в конфе за 7 дней: {messages_amount_per_week}', random_id = random.random())
    messages = lemmatize(messages)
    word_list = set(message_format_and_split(messages))
    print(word_list)

if __name__ == "__main__":
    main()

vk_data_json_file.close()