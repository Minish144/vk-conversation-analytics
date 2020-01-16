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

with open("vk_data.json", "r") as vk_data_json_file:
        vk_data = json.load(vk_data_json_file)

def main():
    pass

if __name__ == "__main__":
    main()

vk_data_json_file.close()