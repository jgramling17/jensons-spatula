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
            stock_status = json_resp["searchedProducts"]["productDetails"][0]["purchaseOption"]
            if stock_status in [self.out_of_stock, ""]:
                no_stock("Nvidia", self.card)
            elif stock_status in [self.check_availability]:
                good_info(f"Nvidia: potential in stock from search-api, {self.card}: {stock_status}")
            elif stock_status in [self.buy_now, self.in_stock, self.add_to_cart]:
                in_stock("Nvidia", self.card)
                send_email(self.personal_info.email,
                           "IN STOCK CARD GET BACK TO COMPUTER",
                           "USE THIS LINK TO TRY AND ADD TO CART AND GET GOING:\n"
                           f"{self.quick_checkout_link}",
                           self.personal_info.botpw)
                return True
        return False

    def aval_api_scrape(self):
        r = requests.get(self.aval_gpu_api_url)
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





