# coding: utf-8
import threading
import time

import click

from BestBuyScraper import BestBuyScraper
from Email import send_email
from Common import *

from PersonalInfo import *


@click.command()
@click.option("--email", required=True, help="Your email address (you wish to be notified during purchase)")
@click.option("--firstname", required=True, help="First Name for Billing and Shipping")
@click.option("--lastname", required=True, help="Last Name for Billing and Shipping")
@click.option("--phonenumber", required=True, help="Phone number WITHOUT dashes")
@click.option("--billingaddress", required=True, help="Address line for credit card")
@click.option("--billingcity", required=True, help="City for credit card")
@click.option("--billingstate", required=True, help="State for credit card")
@click.option("--billingzip", required=True, help="ZIP code for credit card")
@click.option("--creditcard", required=True, help="Credit card")
@click.option("--expirationmonth", required=True, help="Expiration month for Credit card")
@click.option("--expirationyear", required=True, help="Expiration year for Credit card")
@click.option("--ccv", required=True, help="Credit card CCV or security number")
@click.option("--shippingaddress", required=True, help="Address line for shipping")
@click.option("--shippingcity", required=True, help="City for shipping")
@click.option("--shippingstate", required=True, help="State for shipping")
@click.option("--shippingzip", required=True, help="ZIP code for shipping")
@click.option("--botpw", required=True, help="Password for bot's email account")
@click.option("--scrape3070", is_flag=True, help="Enable 3070 scraping")
@click.option("--scrape3080", is_flag=True, help="Enable 3080 scraping")
@click.option("--scrape3080aib", is_flag=True, help="Enable all 3080 scraping including aib")
@click.option("--scrape3090", is_flag=True, help="Enable 3090 scraping")
@click.option("--bestbuyemail", required=False, help="Email for bestbuy account")
@click.option("--bestbuypw", required=False, help="Password for bestbuy account")
@click.option("--bestbuyapikey", required=False, help="Api Key for for bestbuy api account")
@click.option("--dryrun", '-d', is_flag=True, help="enable a dry run to see if your config will run successfully, will not purchase a real card")
def start_bot(email, firstname, lastname, phonenumber, billingaddress, billingcity,
              billingstate, billingzip, creditcard, expirationmonth, expirationyear,
              ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw,
              scrape3070, scrape3080, scrape3080aib, scrape3090, bestbuyemail, bestbuypw, bestbuyapikey,
              dryrun):
    info = make_info(email, firstname, lastname, phonenumber, billingaddress, billingcity,
                     billingstate, billingzip, creditcard, expirationmonth, expirationyear,
                     ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw,
                     bestbuyemail, bestbuypw, bestbuyapikey)
    try:
        scrapers = []
        #Nvidia no longer selling on their site :(
        #Nvidia = NvidiaScraper(info, dryrun)
        #scrapers.append(Nvidia)
        if scrape3070:
            Best_Buy = BestBuyScraper(info, "3070", dryrun)
            scrapers.append(Best_Buy)
        if scrape3080:
            Best_Buy = BestBuyScraper(info, "3080 FE", dryrun)
            scrapers.append(Best_Buy)
        if scrape3080aib:
            Best_Buy = BestBuyScraper(info, "3080 aib", dryrun)
            scrapers.append(Best_Buy)
        if scrape3090:
            Best_Buy = BestBuyScraper(info, "3090", dryrun)
            scrapers.append(Best_Buy)
        a_stop_event = threading.Event()
        if not scrapers:
            warn("You must scrape one card, please use --scrape3070, --scrape3080, and or --scrape3090")
            a_stop_event.set()
        for scrape in scrapers:
            x = threading.Thread(target=scrape.start, args=[a_stop_event], daemon=True)
            x.start()
        while not a_stop_event.is_set():
            # wait for an event
            time.sleep(0.1)
        #used to suspend selenium to keep the browser alive, so the user can double check that it succeeded
        print("It appears the script has ran successfully \n"
              "Please check the browser session for a confirmation page\n"
              "After doing so enter input below")
        end_input = input("WARNING THIS WILL CLOSE BROWSER, press any key followed by enter:")
    except Exception as e:
        send_email(info.email, f"GPU scraper encountered an exception",
                   f"Exception listed below: "
                   f"{e}",
                   info.botpw)

        raise


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_bot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
