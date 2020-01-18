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
    #time_day_ago = time_current-86400
    exit_flag = False
    for i in range(messages_amount_total//200):
        messages_amount_per_week[0]
    #for i in range(15):
        items = vk.messages.getHistory(peer_id=peer_id, count=200, offset=i*200)['items']
        for k in range(200):
            if items[k]['date'] <= time_week_ago:
                exit_flag = True
                break
            messages[0] += items[k]['text'] + ' '
            messages_amount_per_week[0] += 1
        if exit_flag == True:
            break

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

def most_freq_word_in_a_week(word_list):
    word_freq_dict = []
    count = 0
    for primary_word in set(word_list):
        count = 0
        for secondary_word in word_list:
            if primary_word == secondary_word:
                count+=1
        if primary_word == 'люда':
            primary_word = 'люда (не пиши)'
        word_freq_dict.append({"word":primary_word,
                               "amount":count})
    return word_freq_dict

def get_last_message():
    return vk.messages.getHistory(peer_id = peer_id, count = 5)['items'][0]['text']

def main():
    while (1):
        if get_last_message() == 'колб стата':
            try:
                print('готовлю стату')
                vk.messages.send(peer_id=peer_id, random_id = random.random(), message='готовлю стату')
                messages_amount_total = get_messages_total()
                messages_amount_per_week = [0]
                messages = ['']
                get_messages_and_count(messages, messages_amount_per_week, messages_amount_total)
                messages = messages[0]; messages_amount_per_week = messages_amount_per_week[0]
                #messages = lemmatize(messages)
                word_list = message_format_and_split(messages)
                word_freq_dict = most_freq_word_in_a_week(word_list)
                word_freq_dict = list(filter(lambda x : len(x["word"]) > 3, word_freq_dict))
                word_freq_dict = sorted(word_freq_dict, key=lambda k: k['amount'], reverse=True) 
                vk.messages.send(peer_id=peer_id, random_id = random.random(), message=f'Сообщений в конфе всего: {messages_amount_total}\nСообщений в конфе за 7 дней: {messages_amount_per_week}\n-----------------------------------------\nПять самых популярных слов за 7 дней\n{word_freq_dict[0]["word"]} - {word_freq_dict[0]["amount"]} раз \n{word_freq_dict[1]["word"]} - {word_freq_dict[1]["amount"]} раз \n{word_freq_dict[2]["word"]} - {word_freq_dict[2]["amount"]} раз \n{word_freq_dict[3]["word"]} - {word_freq_dict[3]["amount"]} раз \n{word_freq_dict[4]["word"]} - {word_freq_dict[4]["amount"]} раз')
                print(f'Сообщений в конфе всего - {messages_amount_total}\nСообщений в конфе за 7 дней - {messages_amount_per_week}\n-----------------------------------------\nПять самых популярных слов за 7 дней:\n{word_freq_dict[0]["word"]} - {word_freq_dict[0]["amount"]} раз \n{word_freq_dict[1]["word"]} - {word_freq_dict[1]["amount"]} раз \n{word_freq_dict[2]["word"]} - {word_freq_dict[2]["amount"]} раз \n{word_freq_dict[3]["word"]} - {word_freq_dict[3]["amount"]} раз \n{word_freq_dict[4]["word"]} - {word_freq_dict[4]["amount"]} раз')
                #print(word_freq_dict[:20])
            except:
                try:
                    vk.messages.send(peer_id=peer_id, random_id = random.random(), message='привет я сдох')
                except:
                    continue
        if get_last_message().find('колб соси') != -1:
            try:
                vk.messages.send(peer_id=peer_id, random_id = random.random(), message='сам соси')
            except:
                try:
                    vk.messages.send(peer_id=peer_id, random_id = random.random(), message='привет я сдох')
                except:
                    continue

if __name__ == "__main__":
    main()

vk_data_json_file.close()