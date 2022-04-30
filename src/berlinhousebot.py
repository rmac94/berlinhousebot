import requests
from pathlib import Path
import os

import telegram


class ImmoBerlinScrape:

    def __init__(self):
        self.url = "https://www.immobilienscout24.de/Suche/shape/wohnung-mit-einbaukueche-mieten?shape=bWBuX0lxZGBwQWhxQ3l9Q35oRmJqQX5gQG1zRXloQW1gUWRCfX1Fb3hAc2tJY2NJcGhEb25FbEVrekFob0Z1W3hwTnBjQGJiRGpjRH5qRmBMfGdB&numberofrooms=2.0-&price=-1650.0&livingspace=60.0-&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&sorting=2"
        self.historic_id_fp = os.path.join(Path(__file__).parent.parent, 'historic_ids')
        with open(self.historic_id_fp, 'r') as file:
            self.historic_ids = [x.rstrip() for x in file.readlines()]
            file.close()
        self.bot = telegram.BotInstance(r'C:\Users\ronan\OneDrive\Desktop\ImmoBerlinBot.ini')

    def _get_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        req = requests.post(self.url, headers=headers)
        self.results = req.json()['searchResponseModel']['resultlist.resultlist']['resultlistEntries'][0][
            'resultlistEntry']

    def _extract_values(self):
        for residential_property in self.results:
            if residential_property['@id'] not in self.historic_ids:
                message = f"""
                New property Available: {residential_property['resultlist.realEstate']['title']}
                {self.url}
                """
                # self.bot.send_telegram_message(message)
                self.historic_ids.append(residential_property['@id'])

    def _save_records(self):
        with open(self.historic_id_fp, 'w') as file:
            file.writelines(f"{x}\n" for x in self.historic_ids)
            file.close()

    def update(self):
        self._get_html()
        self._extract_values()
        self._save_records()


if __name__ == "__main__":
    immo_instance = ImmoBerlinScrape()
    immo_instance.update()
