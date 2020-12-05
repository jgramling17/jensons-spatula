import time

import requests
from Email import *
from Common import *


class BestBuyApiScraper:
    def __init__(self, personal_info):
        self.card = "3080 FE"
        self.fe_card_sku = "6429440"
        self.aib_found_cards = []
        self.personal_info = personal_info
        self.search_fe_api_url = f"https://api.bestbuy.com/v1/products((search={self.fe_card_sku})&onlineAvailability=true)?apiKey={personal_info.bestbuyapikey}&show=addToCartUrl&format=json"
        self.search_all_api_url = f"https://api.bestbuy.com/v1/products((search=rtx&search=3080)&onlineAvailability=true&(categoryPath.id=abcat0507002))?apiKey={personal_info.bestbuyapikey}&sort=name.asc&show=addToCartUrl,name&pageSize=50&format=json"
        self.search_all_api_url = f"https://api.bestbuy.com/v1/products((search=rtx&search=3080)&(categoryPath.id=abcat0507002))?apiKey={personal_info.bestbuyapikey}&sort=name.asc&show=addToCartUrl,name,url&pageSize=50&format=json"

    def start(self):
        keep_api_scraping = True
        if self.search_fe_api_scrape():
            keep_api_scraping = False
        else:
            time.sleep(5)
        if keep_api_scraping:
            self.search_all_api_scrape()
            time.sleep(60)
        return keep_api_scraping

    def search_fe_api_scrape(self):
        r = requests.get(self.search_fe_api_url)
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

    # This method doesn't return true or false, since it's not our priority to get an AIB card
    def search_all_api_scrape(self):
        r = requests.get(self.search_all_api_url)
        if r.status_code == requests.codes.ok:
            json_resp = r.json()
            if json_resp["products"]:
                email_content = ""
                for prod in json_resp["products"]:
                    name = prod['name']
                    url = prod['addToCartUrl']
                    in_stock("BestBuy", name)
                    if url not in self.aib_found_cards:
                        self.aib_found_cards.append(url)
                        email_content += f"{name}\n{url}\n"
                if email_content != "":
                    send_email(self.personal_info.email,
                               "AIB 3080(s) found",
                               "Use the listed link(s) to add to cart\n"
                               f"{email_content}",
                               self.personal_info.botpw)
                return
            no_stock("BestBuy", "AIB Cards")
        else:
            warn(f"BestBuy Api error: {r.status_code}")
        return

    def get_all_aib_card_urls(self):
        r = requests.get(self.search_all_api_url)
        if r.status_code == requests.codes.ok:
            json_resp = r.json()
            if json_resp["products"]:
                return json_resp["products"]


