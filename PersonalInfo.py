class PersonalInfo:
    def __init__(self, email, firstname, lastname, phonenumber, billingaddress, billingcity,
                 billingstate, billingzip, creditcard, expirationmonth, expirationyear,
                 ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw):
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


def make_info(email, firstname, lastname, phonenumber, billingaddress, billingcity,
              billingstate, billingzip, creditcard, expirationmonth, expirationyear,
              ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw):
    info = PersonalInfo(email, firstname, lastname, phonenumber, billingaddress, billingcity,
                        billingstate, billingzip, creditcard, expirationmonth, expirationyear,
                        ccv, shippingaddress, shippingcity, shippingstate, shippingzip, botpw)
    return info
