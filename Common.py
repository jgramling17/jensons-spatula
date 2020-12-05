from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from colorama import init
from termcolor import colored
from datetime import datetime, date
import logging

from WebDriverEnv import get_webdriver_path

init()


def get_browser(random_user_agent=True):
    web_driver_bin = get_webdriver_path()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
    options = webdriver.ChromeOptions()
    userAgent = get_safe_random_ua() if random_user_agent else get_normal_user_agent()
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("start-maximized");
    options.add_argument("enable-automation");
    options.add_argument("--no-sandbox");
    options.add_argument("--disable-infobars");
    options.add_argument("--disable-dev-shm-usage");
    options.add_argument("--disable-browser-side-navigation");
    options.add_argument("--disable-gpu");
    options.add_argument("--no-proxy-server");
    return webdriver.Chrome(web_driver_bin, chrome_options=options, desired_capabilities=capabilities)


def get_random_user_agent():
    return UserAgent().random


def get_safe_random_ua():
    while True:
        temp = UserAgent().random
        if "Windows NT" not in temp and "CrOS" not in temp:
            return temp


def get_normal_user_agent():
    return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'


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


def init_logger(instance):
    logger = logging.getLogger(instance)
    hdlr = logging.FileHandler(f'./{instance}_network_logs_{date.today()}.json')
    formatter = logging.Formatter('%(message)s\n')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info("[")


def save_network_reqs(driver, instance):
    logs = driver.get_log("performance")
    logger = logging.getLogger(instance)
    for log in logs:
        logger.info(log.get('message') + ",")
    logger.info("]")
