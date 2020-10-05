from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from Email import *
from Common import *
from NvidiaApiScraper import NvidiaApiScraper


class NvidiaScraper:

    def __init__(self, personal_info, dryrun):
        self.personal_info = personal_info
        self.found_card = False
        self.dry_run = dryrun
        self.thirty_eighty_fe_url = "https://www.nvidia.com/en-us/shop/geforce/?page=1&limit=9&locale=en-us&search=NVIDIA%20GEFORCE%20RTX%203080"
        self.thirty_eighty_avail_url = "https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3080/"
        self.quick_checkout_url = "https://store.nvidia.com/store/nvidia/en_US/buy/productID.5438481700/clearCart.yes/nextPage.QuickBuyCartPage"
        self.checkout_url = "https://store.nvidia.com/store?Action=DisplayPage&Env=BASE&Locale=en_US&SiteID=nvidia&id=QuickBuyCartPage"
        self.test = "https://www.nvidia.com/en-us/shop/geforce/?page=1&limit=9&locale=en-us&search=NVIDIA%20GEFORCE%20RTX%202060%20SUPER"
        self.gpu = "3080 FE"
        self.gpu_digital_river_id = "5438481700"
        self.add_to_cart_sel = "a.featured-buy-link"
        self.check_aval_sel = ".extra_style.buy-link"
        self.aval_link_sel = "a.btn-cart.regular-btn"
        self.aval_inner_sel = ".cta-button"
        self.checkout_sel = ".cart__checkout-button"
        self.guest_checkout_sel = "#btnCheckoutAsGuest"
        self.billing_fname_sel = "#billingName1"
        self.billing_lname_sel = "#billingName2"
        self.billing_number_sel = "#billingPhoneNumber"
        self.billing_email_sel = "#email"
        self.billing_email2_sel = "#verEmail"
        self.billing_address_sel = "#billingAddress1"
        self.billing_city_sel = "#billingCity"
        self.billing_state_sel = "#billingState"
        self.billing_zip_sel = "#billingPostalCode"
        self.billing_country_sel = "#billingCountry"
        self.checkbox_sel = "#shippingDifferentThanBilling"
        self.shipping_fname_sel = "#shippingName1"
        self.shipping_lname_sel = "#shippingName2"
        self.shipping_number_sel = "#shippingPhoneNumber"
        self.shipping_address_sel = "#shippingAddress1"
        self.shipping_city_sel = "#shippingCity"
        self.shipping_state_sel = "#shippingState"
        self.shipping_zip_sel = "#shippingPostalCode"
        self.shipping_country_sel = "#shippingCountry"
        self.credit_card_sel = "#ccNum"
        self.credit_month_sel = "#expirationDateMonth"
        self.credit_year_sel = "#expirationDateYear"
        self.credit_ccv_sel = "#cardSecurityCode"
        self.cont_but_sel = "#dr_siteButtons > input.dr_button"
        self.buy_but_sel = "#dr_siteButtons > input.dr_button"

    def start(self, finished_event):
        try:
            self.start_scraping(finished_event)
        except Exception as e:
            send_email(self.personal_info.email, f"GPU scraper encountered an exception",
                       f"Exception listed below: "
                       f"{e}",
                       self.personal_info.botpw)
            raise

    def start_scraping(self, finished_event):
        api_scrape = True
        api_scraper = NvidiaApiScraper(self.personal_info, self.quick_checkout_url)
        while not self.found_card or not finished_event.is_set():
            if api_scrape is True:
                api_scrape = api_scraper.start()
            else:
                self.selenium_scrape(finished_event)

    def selenium_scrape(self, finished_event):
        self.driver = get_browser()
        self.driver.get(self.thirty_eighty_fe_url if not self.dry_run else self.test)
        try:
            buy_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.add_to_cart_sel)))
        except TimeoutException:
            if self.driver.find_element_by_css_selector("span.extra_style.buy-link") is not None:
                check_aval_link = self.driver.find_element_by_css_selector(self.check_aval_sel)
                if "check availability" in check_aval_link.get_attribute('innerHTML').lower():
                    self.check_availability()
                else:
                    good_info("Found a buy now link, which doesn't suggest it's in stock")
            else:
                warn("Loading page took too long")
            self.driver.close()
            return
        if "add to cart" in buy_link.get_attribute('innerHTML').lower():
            in_stock("Nvidia Store", self.gpu)
            self.found_card = True
            print("Attempting to Send Notification to " + self.personal_info.email)
            send_email(self.personal_info.email, f"Found {self.gpu} in stock!",
                       f"Attempting to buy {self.gpu}. "
                       f"Lookout for another email of the success or failure of buying the {self.gpu}",
                       self.personal_info.botpw)
            good_info("Proceeding to buy...")
            buy_link.click()
            checkout_link = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.checkout_sel)))
            checkout_link.click()
            self.buy_card(finished_event)
        else:
            no_stock("Nvidia Store", self.gpu)
            self.driver.close()
            time.sleep(5)
            return

    def check_availability(self):
        info("Checking availability page...")
        self.driver.get(self.thirty_eighty_avail_url)
        aval_link = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.aval_link_sel)))
        if "link-btn-disabled" in aval_link.get_attribute('class').split():
            aval_inner = aval_link.find_element_by_css_selector(self.aval_inner_sel)
            print(aval_inner)
            if "out of stock" in aval_inner.get_attribute('innerHTML').lower():
                info("Availability page out of stock")
            else:
                good_info("Availability NOT out of stock!!!!!!")
                send_email(self.personal_info.email,
                           f"POTENTIAL In Stock {self.gpu}!",
                           "The NVIDIA availability page didn't say Out of Stock\n"
                           "Check computer OR Follow this link to investigate and potentially buy!\n"
                           f"{self.thirty_eighty_avail_url}",
                           self.personal_info.botpw)
                good_info("Attempting to add to cart...")
                aval_link.click()
        else:
            warn("Took too long loading availability page")

    def buy_card(self, finished_event):
        try:
            self.click_guest_checkout()
        except TimeoutException:
            print("Couldn't click on guest checkout trying to manually load checkout page...")
            self.driver.get(self.checkout_url)
            self.click_guest_checkout()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.billing_fname_sel)))
        print("Filling out info form...")
        fill_out_textbox(self.driver, self.billing_fname_sel, self.personal_info.firstname)
        fill_out_textbox(self.driver, self.billing_lname_sel, self.personal_info.lastname)
        fill_out_textbox(self.driver, self.billing_number_sel, self.personal_info.phonenumber)
        fill_out_textbox(self.driver, self.billing_address_sel, self.personal_info.billingaddress)
        fill_out_textbox(self.driver, self.billing_city_sel, self.personal_info.billingcity)
        fill_out_textbox(self.driver, self.billing_zip_sel, self.personal_info.billingzip)
        fill_out_textbox(self.driver, self.billing_email_sel, self.personal_info.email)
        fill_out_textbox(self.driver, self.billing_email2_sel, self.personal_info.email)
        pick_dropdown(self.driver, self.billing_country_sel, "US")
        pick_dropdown(self.driver, self.billing_state_sel, self.personal_info.billingstate)

        self.driver.find_element_by_css_selector(self.checkbox_sel).click()
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.shipping_fname_sel)))

        fill_out_textbox(self.driver, self.shipping_fname_sel, self.personal_info.firstname)
        fill_out_textbox(self.driver, self.shipping_lname_sel, self.personal_info.lastname)
        fill_out_textbox(self.driver, self.shipping_number_sel, self.personal_info.phonenumber)
        fill_out_textbox(self.driver, self.shipping_address_sel, self.personal_info.shippingaddress)
        fill_out_textbox(self.driver, self.shipping_city_sel, self.personal_info.shippingcity)
        fill_out_textbox(self.driver, self.shipping_zip_sel, self.personal_info.shippingzip)
        pick_dropdown(self.driver, self.shipping_country_sel, "US")
        pick_dropdown(self.driver, self.shipping_state_sel, self.personal_info.shippingstate)

        fill_out_textbox(self.driver, self.credit_card_sel, self.personal_info.creditcard)
        fill_out_textbox(self.driver, self.credit_ccv_sel, self.personal_info.ccv)
        pick_dropdown(self.driver, self.credit_month_sel, self.personal_info.expirationmonth)
        pick_dropdown(self.driver, self.credit_year_sel, self.personal_info.expirationyear)

        self.driver.find_element_by_css_selector(self.cont_but_sel).click()

        print(f"Form filled out successfully, about to buy {self.gpu}.")
        send_email(self.personal_info.email, f"ATTENTION: About to buy...",
                   f"BE READY TO CHECK COMPUTER!!!!! Form filled out successfully, about to buy {self.gpu}. "
                   f" {self.gpu}",
                   self.personal_info.botpw)

        #Hacky way that fakes a captcha finished, unproven method, just enables the checkout button
        self.driver.execute_script("onloadCallback();")

        FINAL_BUY_BUTTON = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.buy_but_sel)))

        if not self.dry_run:
            FINAL_BUY_BUTTON.click()
            finished_event.set()
        else:
            print("dry_run is enabled, will not proceed with checking out")
            finished_event.set()

    def click_guest_checkout(self):
        guest_checkout_link = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.guest_checkout_sel)))
        guest_checkout_link.click()
