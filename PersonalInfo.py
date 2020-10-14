class PersonalInfo:
    def __init__(self, email, firstname, lastname, phonenumber, billingaddress, billingcity,
                 billingstate, billingzip, creditcard, expirationmonth, expirationyear,
                 ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw,
                 bestbuyemail, bestbuypw, bestbuyapikey):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phonenumber = phonenumber
        self.billingaddress = billingaddress
        self.billingcity = billingcity
        self.billingstate = billingstate
        self.billingzip = billingzip
        self.creditcard = creditcard
        self.expirationmonth = expirationmonth
        self.expirationyear = expirationyear
        self.ccv = ccv
        self.shippingaddress = shippingaddress
        self.shippingcity = shippingcity
        self.shippingstate = shippingstate
        self.shippingzip = shippingzip
        self.botpw = botpw
        self.bestbuyemail = bestbuyemail
        self.bestbuypw = bestbuypw
        self.bestbuyapikey = bestbuyapikey


def make_info(email, firstname, lastname, phonenumber, billingaddress, billingcity,
              billingstate, billingzip, creditcard, expirationmonth, expirationyear,
              ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw,
              bestbuyemail, bestbuypw, bestbuyapikey):
    info = PersonalInfo(email, firstname, lastname, phonenumber, billingaddress, billingcity,
                        billingstate, billingzip, creditcard, expirationmonth, expirationyear,
                        ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw,
                        bestbuyemail, bestbuypw, bestbuyapikey)
    if info.bestbuyemail is None or info.bestbuypw is None or info.bestbuyapikey is None:
        raise Exception("No bestbuy username or password found or apikey")
    return info
