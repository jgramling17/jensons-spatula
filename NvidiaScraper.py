from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from WebDriverEnv import get_webdriver_path
from Email import *



class NvidiaScraper:

    def __init__(self, personal_info, dryrun):
        self.web_driver_bin = get_webdriver_path()
        self.personal_info = personal_info
        self.found_card = False
        self.dry_run = dryrun
        self.thirty_eighty_fe_url = "https://www.nvidia.com/en-us/shop/geforce/?page=1&limit=9&locale=en-us&search=NVIDIA%20GEFORCE%20RTX%203080"
        self.test = "https://www.nvidia.com/en-us/shop/geforce/?page=1&limit=9&locale=en-us&search=NVIDIA%20GEFORCE%20RTX%202060%20SUPER"
        self.add_to_cart_sel = "a.featured-buy-link"
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
        self.gpu = "3080 FE"

    def start(self):
        while not self.found_card:
            options = Options()
            ua = UserAgent()
            userAgent = ua.random
            options.add_argument(f'user-agent={userAgent}')
            self.driver = webdriver.Chrome(self.web_driver_bin, chrome_options=options)
            self.driver.maximize_window()
            self.driver.get(self.thirty_eighty_fe_url if not self.dry_run else self.test)
            try:
                buy_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.add_to_cart_sel)))
            except TimeoutException:
                if self.driver.find_element_by_css_selector("span.extra_style.buy-link") is not None:
                    print("Found a buy now link, which doesn't suggest it's in stock")
                else:
                    print("Loading page took too long")
                self.driver.close()
                continue
            if "add to cart" in buy_link.get_attribute('innerHTML').lower():
                print(f"{self.gpu} in stock")
                self.found_card = True
                print("Attempting to Send Notification to " + self.personal_info.email)
                send_email(self.personal_info.email, f"Found {self.gpu} in stock!",
                           f"Attempting to buy {self.gpu}. "
                           f"Lookout for another email of the success or failure of buying the {self.gpu}",
                           self.personal_info.botpw)
                print("Proceeding to buy...")
                buy_link.click()
                checkout_link = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.checkout_sel)))
                checkout_link.click()
                self.buy_card()
            else:
                print("Not in stock")
                self.driver.close()
                time.sleep(5)

    def buy_card(self):
        guest_checkout_link = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.guest_checkout_sel)))
        guest_checkout_link.click()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.billing_fname_sel)))
        print("Filling out info form...")
        self.fill_out_textbox(self.billing_fname_sel, self.personal_info.firstname)
        self.fill_out_textbox(self.billing_lname_sel, self.personal_info.lastname)
        self.fill_out_textbox(self.billing_number_sel, self.personal_info.phonenumber)
        self.fill_out_textbox(self.billing_address_sel, self.personal_info.billingaddress)
        self.fill_out_textbox(self.billing_city_sel, self.personal_info.billingcity)
        self.fill_out_textbox(self.billing_zip_sel, self.personal_info.billingzip)
        self.fill_out_textbox(self.billing_email_sel, self.personal_info.email)
        self.fill_out_textbox(self.billing_email2_sel, self.personal_info.email)
        self.pick_dropdown(self.billing_country_sel, "US")
        self.pick_dropdown(self.billing_state_sel, self.personal_info.billingstate)

        self.driver.find_element_by_css_selector(self.checkbox_sel).click()
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.shipping_fname_sel)))

        self.fill_out_textbox(self.shipping_fname_sel, self.personal_info.firstname)
        self.fill_out_textbox(self.shipping_lname_sel, self.personal_info.lastname)
        self.fill_out_textbox(self.shipping_number_sel, self.personal_info.phonenumber)
        self.fill_out_textbox(self.shipping_address_sel, self.personal_info.shippingaddress)
        self.fill_out_textbox(self.shipping_city_sel, self.personal_info.shippingcity)
        self.fill_out_textbox(self.shipping_zip_sel, self.personal_info.shippingzip)
        self.pick_dropdown(self.shipping_country_sel, "US")
        self.pick_dropdown(self.shipping_state_sel, self.personal_info.shippingstate)

        self.fill_out_textbox(self.credit_card_sel, self.personal_info.creditcard)
        self.fill_out_textbox(self.credit_ccv_sel, self.personal_info.ccv)
        self.pick_dropdown(self.credit_month_sel, self.personal_info.expirationmonth)
        self.pick_dropdown(self.credit_year_sel, self.personal_info.expirationyear)

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
            #FINAL_BUY_BUTTON.click()
            print("Would have clicked the button")
        else:
            print("dry_run is enabled, will not proceed with checking out")

    def fill_out_textbox(self, sel, text):
        self.driver.find_element_by_css_selector(sel).send_keys(text)

    def pick_dropdown(self, sel, val):
        dropdown = Select(self.driver.find_element_by_css_selector(sel))
        dropdown.select_by_value(val)