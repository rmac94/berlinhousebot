import configparser
import json

import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BotInstance:
    def __init__(self, ini_location):
        self.ini_location = ini_location
        config = configparser.ConfigParser()
        config.read(self.ini_location)
        self.chat_id = config['DEFAULT']['chat_id']
        self.api_key = config['DEFAULT']['api_key']

    def send_telegram_message(self, message: str):

        headers = {'Content-Type': 'application/json',
                   'Proxy-Authorization': 'Basic base64'}
        data_dict = {'chat_id': self.chat_id,
                     'text': message,
                     'parse_mode': 'HTML',
                     'disable_notification': True}
        data = json.dumps(data_dict)
        url = f'https://api.telegram.org/bot{self.api_key}/sendMessage'
        response = requests.post(url,
                                 data=data,
                                 headers=headers,
                                 verify=False)
        return response


if __name__ == "__main__":
    bot = BotInstance(r'C:\Users\ronan\OneDrive\Desktop\ImmoBerlinBot.ini')
    bot.send_telegram_message("Hello world")
