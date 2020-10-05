import time

import requests
from Email import *
from Common import *


class BestBuyApiScraper:
    def __init__(self, personal_info):
        self.card = "3080 FE"
        self.personal_info = personal_info
        self.search_gpu_api_url = f"https://api.bestbuy.com/v1/products((search=6429440)&onlineAvailability=true)?apiKey={personal_info.bestbuyapikey}&show=addToCartUrl&format=json"

    def start(self):
        keep_api_scraping = True
        if self.search_api_scrape():
            keep_api_scraping = False
        else:
            time.sleep(60)
        return keep_api_scraping

    def search_api_scrape(self):
        r = requests.get(self.search_gpu_api_url)
        if r.status_code == requests.codes.ok:
            json_resp = r.json()
            if json_resp["products"]:
                cart_url = json_resp["products"][0]["addToCartUrl"]
                if cart_url:
                    in_stock("BestBuy", self.card)
                    send_email(self.personal_info.email,
                               "IN STOCK CARD GET BACK TO COMPUTER",
                               "USE THIS LINK TO TRY AND ADD TO CART AND GET GOING:\n"
                               f"{cart_url}",
                               self.personal_info.botpw)
                    return True
            no_stock("BestBuy", self.card)
        else:
            warn(f"BestBuy Api error: {r.status_code}")
        return False
