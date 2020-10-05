import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BestBuyApiScraper import BestBuyApiScraper
from Common import *
from Email import send_email


class BestBuyScraper:

    def __init__(self, personal_info, dryrun):
        self.personal_info = personal_info
        self.found_card = False
        self.dry_run = dryrun
        self.thirty_eighty_fe_url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"
        self.test = "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-2060-super-8gb-gddr6-pci-express-3-0-graphics-card-black-gray/6397799.p?skuId=6397799"
        self.checkout_url = "https://www.bestbuy.com/cart/c/"
        self.add_to_cart_sel = "div.col-xs-5.col-lg-4 button.add-to-cart-button"
        self.go_to_cart_sel = "div.c-modal-grid.col-xs-10 div.go-to-cart-button"
        self.checkout_sel = "button[data-track='Checkout - Top']"
        self.shipping_radio_sel = "div.availability__fulfillment"
        self.account_email_sel = "input#fld-e"
        self.account_pw_sel = "input#fld-p1"
        self.sign_in_sel = "[type='submit']"
        self.gpu = "3080 FE"

    def start(self, finished_event):
        try:
            self.start_scraping(finished_event)
        except Exception as e:
            send_email(self.personal_info.email, f"GPU scraper encountered an exception",
                       f"Exception listed below: "
                       f"{e}",
                       self.personal_info.email)
            raise

    def start_scraping(self, finished_event):
        api_scrape = True
        api_scraper = BestBuyApiScraper(self.personal_info)
        while not self.found_card or not finished_event.is_set():
            if api_scrape is True:
                api_scrape = api_scraper.start()
            else:
                #JOEL TODO ADD BEST BUY ADD TO CART LINK TO THIS METHOD
                self.selenium_scrape(finished_event)

    def selenium_scrape(self, finished_event):
        self.driver = get_browser()
        self.driver.get(self.thirty_eighty_fe_url if not self.dry_run else self.test)
        try:
            buy_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.add_to_cart_sel)))
        except TimeoutException:
            warn("Loading page took too long")
            self.driver.close()
            return
        if "add to cart" in buy_link.get_attribute('innerHTML').lower():
            in_stock("Best Buy", self.gpu)
            self.found_card = True
            print("Attempting to Send Notification to " + self.personal_info.email)
            send_email(self.personal_info.email, f"Found {self.gpu} in stock!",
                       f"Attempting to buy {self.gpu}. "
                       f"Lookout for another email of the success or failure of buying the {self.gpu}",
                       self.personal_info.botpw)
            good_info("Proceeding to buy...")
            buy_link.click()
            cart_link = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.go_to_cart_sel)))
            cart_link.click()
            checkout_link = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.checkout_sel)))
            checkout_link.click()
            self.buy_card(finished_event)
        else:
            no_stock("Best Buy", self.gpu)
            self.driver.close()
            time.sleep(5)
            return

    def buy_card(self, finished_event):
        try:
            self.checkout_sign_in()
        except TimeoutException:
            print("Couldn't click on guest checkout trying to manually load checkout page...")
            self.driver.get(self.checkout_url)
            self.checkout_sign_in()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.billing_fname_sel)))
        print("Filling out info form...")

    def checkout_sign_in(self):
        time.sleep(5)
        shipping_radio = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.shipping_radio_sel)))
        shipping_radio.click()
        checkout_link = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.checkout_sel)))
        checkout_link.click()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.account_email_sel)))
        fill_out_textbox(self.driver, self.account_email_sel, self.personal_info.bestbuyemail)
        fill_out_textbox(self.driver, self.account_pw_sel, self.personal_info.bestbuypw)
        self.driver.find_element_by_css_selector(self.sign_in_sel).click()
        time.sleep(100)

