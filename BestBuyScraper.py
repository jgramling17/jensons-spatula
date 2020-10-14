import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BestBuyApiScraper import BestBuyApiScraper
from Common import *
from Email import send_email


class BestBuyScraper:

    def __init__(self, personal_info, card, dryrun):
        self.personal_info = personal_info
        if len(self.personal_info.expirationmonth) == 1:
            self.personal_info.expirationmonth = '0' + self.personal_info.expirationmonth
        self.found_card = False
        self.dry_run = dryrun
        self.thirty_seventy_fe_url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
        self.thirty_eighty_fe_url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"
        self.thirty_ninety_fe_url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434"
        self.card_url = ""
        if card == "3070":
            self.card_url = self.thirty_seventy_fe_url
        elif card == "3080":
            self.card_url = self.thirty_eighty_fe_url
        elif card == "3090":
            self.card_url = self.thirty_ninety_fe_url
        self.test = "https://www.bestbuy.com/site/wd-wd_black-sn750-nvme-500gb-internal-pci-express-3-0-x4-solid-state-drive-for-laptops-desktops/6338994.p?skuId=6338994"
        self.checkout_url = "https://www.bestbuy.com/cart/c/"
        self.add_to_cart_sel = "div.col-xs-5.col-lg-4 button.add-to-cart-button"
        self.go_to_cart_sel = "div.c-modal-grid.col-xs-10 div.go-to-cart-button"
        self.checkout_sel = "button[data-track='Checkout - Top']"
        self.shipping_radio_sel = "input[id^=fulfillment-shipping]"
        self.spinner_sel = ".page-spinner--in"
        self.account_email_sel = "input#fld-e"
        self.account_pw_sel = "input#fld-p1"
        self.sign_in_sel = "[type='submit']"
        self.payment_continue_sel = ".button--continue > button.btn.btn-lg.btn-block,btn-secondary"
        self.credit_card_sel = "#optimized-cc-card-number"
        self.exp_mo_sel = "select[name=expiration-month]"
        self.exp_yr_sel = "select[name=expiration-year]"
        self.ccv_sel = "input#credit-card-cvv"
        self.FINAL_BUTTON_SEL = ".button--place-order > button.btn.btn-lg.btn-block.btn-primary"
        self.gpu = f"{card} FE"

    def start(self, finished_event):
        try:
            self.start_scraping(finished_event)
        except Exception as e:
            send_email(self.personal_info.email, f"GPU scraper encountered an exception",
                       f"Exception listed below: "
                       f"{e}",
                       self.personal_info.email)
            raise

    #API WAS BEHIND BY 10 MINUTES, NO LONGER TRUSTING THIS
    def start_scraping_deprecated(self, finished_event):
        api_scrape = True
        api_scraper = BestBuyApiScraper(self.personal_info)
        while not self.found_card or not finished_event.is_set():
            if api_scrape is True:
                api_scrape = api_scraper.start()
            else:
                #JOEL TODO ADD BEST BUY ADD TO CART LINK TO THIS METHOD
                self.selenium_scrape(finished_event)

    def start_scraping(self, finished_event):
        while not self.found_card and not finished_event.is_set():
            self.selenium_scrape(finished_event)

    def selenium_scrape(self, finished_event):
        self.driver = get_browser(random_user_agent=False)
        self.driver.get(self.card_url if not self.dry_run else self.test)
        try:
            buy_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.add_to_cart_sel)))
        except TimeoutException:
            button = self.driver.find_element_by_css_selector(self.add_to_cart_sel)
            if button.is_displayed() and not button.is_enabled():
                no_stock("Best Buy", self.gpu)
            else:
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
            self.buy_card(finished_event)
        else:
            no_stock("Best Buy", self.gpu)
            self.driver.close()
            time.sleep(5)
            return

    def buy_card(self, finished_event):
        try:
            self.checkout_sign_in()
        except TimeoutException as e:
            print("Couldn't click on guest checkout trying to manually load checkout page...")
            self.driver.get(self.checkout_url)
            self.checkout_sign_in()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.payment_continue_sel))).click()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.credit_card_sel)))
        fill_out_textbox(self.driver, self.credit_card_sel, self.personal_info.creditcard)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.exp_mo_sel)))
        pick_dropdown(self.driver, self.exp_mo_sel, self.personal_info.expirationmonth)
        pick_dropdown(self.driver, self.exp_yr_sel, self.personal_info.expirationyear)
        fill_out_textbox(self.driver, self.ccv_sel, self.personal_info.ccv)

        print(f"Form filled out successfully, about to buy {self.gpu}.")
        send_email(self.personal_info.email, f"ATTENTION: About to buy...",
                   f"BE READY TO CHECK COMPUTER!!!!! Form filled out successfully, about to buy {self.gpu}. "
                   f" {self.gpu}",
                   self.personal_info.botpw)
        FINAL_BUY_BUTTON = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.FINAL_BUTTON_SEL)))

        if not self.dry_run:
            FINAL_BUY_BUTTON.click()
            finished_event.set()
        else:
            print("dry_run is enabled, will not proceed with checking out")
            finished_event.set()


    def checkout_sign_in(self):
        shipping_radio = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.shipping_radio_sel)))
        shipping_radio.click()
        self.wait_for_spinner(self.spinner_sel)
        checkout_link = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.checkout_sel)))
        checkout_link.click()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.account_email_sel)))
        fill_out_textbox(self.driver, self.account_email_sel, self.personal_info.bestbuyemail)
        fill_out_textbox(self.driver, self.account_pw_sel, self.personal_info.bestbuypw)
        self.driver.find_element_by_css_selector(self.sign_in_sel).click()

    def wait_for_spinner(self, sel_vis):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element((By.CSS_SELECTOR, sel_vis)))
        except TimeoutException:
            #do nothing
            pass


