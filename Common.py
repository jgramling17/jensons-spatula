from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from fake_useragent import UserAgent
from colorama import init
from termcolor import colored
from datetime import datetime

from WebDriverEnv import get_webdriver_path

init()


def get_browser():
    web_driver_bin = get_webdriver_path()
    options = webdriver.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("start-maximized");
    options.add_argument("enable-automation");
    options.add_argument("--no-sandbox");
    options.add_argument("--disable-infobars");
    options.add_argument("--disable-dev-shm-usage");
    options.add_argument("--disable-browser-side-navigation");
    options.add_argument("--disable-gpu");
    options.add_argument("--no-proxy-server");
    return webdriver.Chrome(web_driver_bin, chrome_options=options)

def fill_out_textbox(driver, sel, text):
    driver.find_element_by_css_selector(sel).send_keys(text)

def pick_dropdown(driver, sel, val):
    dropdown = Select(driver.find_element_by_css_selector(sel))
    dropdown.select_by_value(val)

def info(str):
    print(f"{colored(datetime.now(), 'cyan')} {colored(str, 'yellow')}")

def warn(str):
    print(f"{colored(datetime.now(), 'cyan')} {colored(str, 'red')}")

def good_info(str):
    print(f"{colored(datetime.now(), 'cyan')} {colored(str, 'green')}")

def no_stock(retailer, card):
    print(f"{colored(datetime.now(), 'cyan')} {retailer} {card} [{colored('NO STOCK', 'red')}]")

def in_stock(retailer, card):
    print(f"{colored(datetime.now(), 'cyan')} {retailer} {card} [{colored('IN STOCK', 'green')}]")