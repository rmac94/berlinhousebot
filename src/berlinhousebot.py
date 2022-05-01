import requests
from pathlib import Path
import os
import re

from bs4 import BeautifulSoup

import telegram


class ImmoBerlinScrape:

    def __init__(self, url: str):
        self.url = url
        self.website = re.findall(r"www\.(.*)\.de.*", url)[0]
        self.current_ids = []
        self.historic_id_fp = os.path.join(Path(__file__).parent.parent, 'historic_ids')
        with open(self.historic_id_fp, 'r+') as file:
            self.historic_ids = [x.rstrip() for x in file.readlines()]
            file.close()
        self.bot = telegram.BotInstance(os.path.join(
                                                    os.path.expanduser('~'),
                                                    'ImmoBerlinBot.ini')
                                        )

    def _get_and_parse_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept-Language': 'en-US,en;q=0.5'
        }

        if self.website == "immobilienscout24":
            req = requests.post(self.url, headers=headers).json()
            self.results =req['searchResponseModel']['resultlist.resultlist']['resultlistEntries'][0]['resultlistEntry']
            for ad in self.results:
                self.current_ids.append(ad['@id'])
        else:
            req = requests.get(self.url, headers=headers)
            self.results = BeautifulSoup(req.content, 'html.parser').find_all("article", class_= "aditem")
            for ad in self.results:
                self.current_ids.append(ad.get('data-adid'))

    def _send_notification(self):
        for id in self.current_ids:
            if id not in self.historic_ids:
                message = f"""
                New property Available:
                {self.url}
                """
                self.bot.send_telegram_message(message)
                self.historic_ids.append(id)

    def _save_records(self):
        with open(self.historic_id_fp, 'w') as file:
            file.writelines(f"{x}\n" for x in self.historic_ids)
            file.close()

    def update(self):
        self._get_and_parse_html()
        self._send_notification()
        self._save_records()


if __name__ == "__main__":
    for url in ["https://www.immobilienscout24.de/Suche/shape/wohnung-mit-einbaukueche-mieten?shape=bWBuX0lxZGBwQWhxQ3l9Q35oRmJqQX5gQG1zRXloQW1gUWRCfX1Fb3hAc2tJY2NJcGhEb25FbEVrekFob0Z1W3hwTnBjQGJiRGpjRH5qRmBMfGdB&numberofrooms=2.0-&price=-1650.0&livingspace=60.0-&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&sorting=2",
                "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/c203l3331+wohnung_mieten.qm_d:65.00%2C+wohnung_mieten.swap_s:nein+wohnung_mieten.zimmer_d:2.5%2C"]:
        immo_instance = ImmoBerlinScrape(url=url)
        immo_instance.update()
