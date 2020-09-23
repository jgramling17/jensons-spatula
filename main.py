# coding: utf-8
import click

from Email import send_email
from NvidiaScraper import NvidiaScraper

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
@click.option("--dryrun", '-d', is_flag=True, help="enable a dry run to see if your config will run successfully, will not purchase a real card")

def start_bot(email, firstname, lastname, phonenumber, billingaddress, billingcity,
              billingstate, billingzip, creditcard, expirationmonth, expirationyear,
              ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw, dryrun):
    info = make_info(email, firstname, lastname, phonenumber, billingaddress, billingcity,
                     billingstate, billingzip, creditcard, expirationmonth, expirationyear,
                     ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw)
    fe = NvidiaScraper(info, dryrun)
    try:
        fe.start()
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
