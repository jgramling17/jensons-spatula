import time

import requests
from Email import *
from Common import *


class NvidiaApiScraper:
    def __init__(self, personal_info, quick_checkout_link):
        self.experimental_api_down_notification = 0
        self.experimental_api_up_notification = 0
        self.card = "3080 FE"
        self.personal_info = personal_info
        self.aval_gpu_api_url = "https://api-prod.nvidia.com/direct-sales-shop/DR/products/en_us/USD/5438481700"
        self.search_gpu_api_url = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-us&search=NVIDIA%20GEFORCE%20RTX%203080"
        self.quick_checkout_link = quick_checkout_link
        self.out_of_stock = "out_of_stock"
        self.check_availability = "check_availability"
        self.buy_now = "buy_now"
        self.in_stock = "in_stock"
        self.add_to_cart = "add_to_cart"

    def start(self):
        keep_api_scraping = True
        if self.search_api_scrape():
            keep_api_scraping = False
        else:
            time.sleep(5)
        if keep_api_scraping:
            if self.aval_api_scrape():
                keep_api_scraping = False
            else:
                time.sleep(5)
        return keep_api_scraping

    def search_api_scrape(self):
        r = requests.get(self.search_gpu_api_url)
        if r.status_code == requests.codes.ok:
            json_resp = r.json()
            product = json_resp["searchedProducts"]["productDetails"][0]
            stock_status = product["purchaseOption"]
            product_status = product["prdStatus"]
            if stock_status in [self.out_of_stock, ""] and product_status not in [self.check_availability]:
                no_stock("Nvidia", self.card)
            elif product_status in [self.check_availability]:
                info(f"Nvidia: potential in stock from search-api, {self.card}: {stock_status}")
                self.search_api_retailer_parse(product["retailers"])
            elif stock_status in [self.buy_now, self.in_stock, self.add_to_cart]:
                in_stock("Nvidia", self.card)
                send_email(self.personal_info.email,
                           "IN STOCK CARD GET BACK TO COMPUTER",
                           "USE THIS LINK TO TRY AND ADD TO CART AND GET GOING:\n"
                           f"{self.quick_checkout_link}",
                           self.personal_info.botpw)
                return True
        return False

    def search_api_retailer_parse(self, retailers):
        for offer in retailers:
            #Our bestbuy api scraper will handle this
            if offer["partnerId"] == '2':
                continue
            #Nvidia
            elif offer["partnerId"] == '111':
                if offer["stock"] != 0 or offer["isAvailable"] or offer["directPurchaseLink"] is not None:
                    in_stock("Nvidia", self.card)
                    send_email(self.personal_info.email,
                               "IN STOCK CARD GET BACK TO COMPUTER",
                               "USE THIS LINK TO TRY AND ADD TO CART AND GET GOING:\n"
                               f"regular link: {offer['purchaseLink']}\n"
                               f"direct purchase link: {offer['directPurchaseLink']}\n",
                               self.personal_info.botpw)
                else:
                    no_stock("Nvidia", self.card)



    def aval_api_scrape(self):
        payload = {}
        headers = {
            'authority': 'api-prod.nvidia.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': get_random_user_agent(),
            'dnt': '1',
            'origin': 'https://www.nvidia.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3080/',
            'accept-language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        r = requests.request("GET", self.aval_gpu_api_url, headers=headers, data=payload)
        if r.status_code == requests.codes.ok:
            good_info("Nvidia Api is up!")
            if self.experimental_api_up_notification < 1:
                send_email(self.personal_info.email,
                           f"Experimental email",
                           "The Api is up and running, please inspect for future reference\n"
                           f"{self.quick_checkout_link}",
                           self.personal_info.botpw)
                self.experimental_api_up_notification += 1
                with open('api_response.json', 'w') as file:
                    file.write(str(r.json()))
                return True
            else:
                warn("Joel you dumb motherfucker, implement api checking")
                return True
        else:
            warn(f"Nvidia Api is down: {r.status_code}")
            if self.experimental_api_down_notification < 1:
                send_email(self.personal_info.email,
                           f"Experimental email",
                           "The Api is down, return to your computer to inspect\n"
                           f"{self.quick_checkout_link}",
                           self.personal_info.botpw)
                self.experimental_api_down_notification += 1
        return False





