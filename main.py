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
    for i in range(messages_amount_total//200):
    #for i in range(15):
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

def most_freq_word_in_a_week(word_list):
    word_freq_dict = []
    count = 0
    for primary_word in set(word_list):
        count = 0
        for secondary_word in word_list:
            if primary_word == secondary_word:
                count+=1
        word_freq_dict.append({"word":primary_word,
                               "amount":count})
    return word_freq_dict

def main():
    messages_amount_total = get_messages_total()
    messages_amount_per_week = [0]
    messages = ['']
    get_messages_and_count(messages, messages_amount_per_week, messages_amount_total)
    messages = messages[0]; messages_amount_per_week = messages_amount_per_week[0]
    print('сообщений в конфе за 7 дней:', messages_amount_per_week)
    messages = lemmatize(messages)
    word_list = message_format_and_split(messages)
    word_freq_dict = most_freq_word_in_a_week(word_list)
    word_freq_dict = list(filter(lambda x : len(x["word"]) > 3, word_freq_dict))
    word_freq_dict = sorted(word_freq_dict, key=lambda k: k['amount'], reverse=True) 
    print(word_freq_dict)

    vk.messages.send(peer_id=peer_id, random_id = random.random(), message=f'Сообщений в конфе всего: {messages_amount_total}\nСообщений в конфе за 7 дней: {messages_amount_per_week}\nПять самых популярных слов за 7 дней: \n{word_freq_dict[0]["word"]} - {word_freq_dict[0]["amount"]} раз \n{word_freq_dict[1]["word"]} - {word_freq_dict[1]["amount"]} раз \n{word_freq_dict[2]["word"]} - {word_freq_dict[2]["amount"]} раз \n{word_freq_dict[3]["word"]} - {word_freq_dict[3]["amount"]} раз \n{word_freq_dict[4]["word"]} - {word_freq_dict[4]["amount"]} раз')


if __name__ == "__main__":
    main()

vk_data_json_file.close()