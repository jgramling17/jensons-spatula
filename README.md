# jensons-spatula

Jenson's spatula does a specific thing via python and selenium

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Jenson's Spatula.

Mac
```bash
pip3 install -r requirements.txt
```
Windows
```bash
pip install -r requirements.txt
```

## Usage
Create yourself a 'config' file to run from the command line

Example file:
```bash
python3 main.py
--email youremail@aol.com 
--firstname John 
--lastname Smith 
--phonenumber 2025550124 
--billingaddress "100 Redwood Dr" 
--billingcity Venetia 
--billingstate PA 
--billingzip 15367-0001
--creditcard 1000100010001000
--expirationmonth 9 
--expirationyear 2069
--ccv 111
--shippingaddress "100 Redwood Dr"
--shippingcity Venetia
--shippingstate PA
--shippingzip 15367-0001
--botpw YouHaveToAskMeForThis
```
### Extra flags
--dryrun (-d)

Used to see if all your information is validated properly. It will add a 2060 super to your cart and proceed to checkout, it will not purchase.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)