import tkinter as tk
from tkinter import ttk
import time
import requests
import json
import re

account = '#########'
api_id = '##########'
api_pass = '########'

def getpayeerblnc(account, api_id, api_pass):
    p = PayeerAPI(account, api_id, api_pass)

    js = p.get_balance()
    myblncbtc = json.dumps(js['BTC'] ['BUDGET'])
    myblncbtc = myblncbtc.replace('"', "")
    return myblncbtc


def getbtc():
    req1 = requests.get('https://blockchain.info/ticker')
    req01 = req1.json()
    blockchain = json.dumps(req01['USD'] ['buy'], indent=2)
    blockchain = str(blockchain)
    return blockchain    

def calculate_blnc(myblncbtc, blockchain):
    blnc2 = float(blockchain)
    blnc2 = blnc2 -150
    myblncbtc = float(myblncbtc)
    balance2 = blnc2 * myblncbtc
    balance2 = round(balance2, 2)
    return str(balance2) + str(' $')

class Currency(tk.Tk):
    def __init__(self):
        super().__init__()

        self.label = ttk.Label(
            text=str('PAYEER: ') + calculate_blnc(getpayeerblnc(account, api_id, api_pass), getbtc()),
            font=('Digital-7', 30))

        self.label.pack(expand=True)

        self.label2 = ttk.Label(
            text=str('BTC: ') + getbtc() + str(' $'), 
            font=('Digital-7', 30),
            foreground='#00FFFF')

        self.label2.pack(expand=True)

        self.title('Currency')
        self.resizable(0, 0)
        self.geometry('270x125')
        self['bg'] = 'black'

        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='#00FF00')


        self.label.after(1000000, self.update)
        self.label2.after(1000000, self.update)

    def update(self):
        balance2 = self.calculate_blnc(self.getpayeerblnc(account, api_id, api_pass), self.getbtc())
        balance2 = round(balance2, 2)
        balance2 = str('PAYEER: ') + str(balance2) + str(' $')
        rate = self.getbtc()
        rate = str('BTC: ') + rate + str(' $')
        self.label.configure(text=balance2)
        self.label2.configure(text=rate)

        self.label.after(1000000, self.update)
        self.label2.after(1000000, self.update)


    def getpayeerblnc(self, account, api_id, api_pass):
        p = PayeerAPI(account, api_id, api_pass)

        js = p.get_balance()
        myblncbtc = json.dumps(js['BTC'] ['BUDGET'])
        myblncbtc = myblncbtc.replace('"', "")
        return myblncbtc


    def getbtc(self):
        req1 = requests.get('https://blockchain.info/ticker')
        req01 = req1.json()
        blockchain = json.dumps(req01['USD'] ['buy'], indent=2)
        blockchain = str(blockchain)
        return blockchain

    def calculate_blnc(self, myblncbtc, blockchain):
        blnc2 = float(blockchain)
        blnc2 = blnc2 -150
        myblncbtc = float(myblncbtc)
        balance2 = blnc2 * myblncbtc
        return balance2


def validate_wallet(wallet):
    if not re.match('P\d{7,12}$', wallet):
        raise ValueError('Wrong wallet format!')

class PayeerAPIException(Exception):
    """Base payeer api exception class"""

class PayeerAPI:
    """Payeer API Client"""

    def __init__(self, account, apiId, apiPass):
        validate_wallet(account)
        self.account = account
        self.apiId = apiId
        self.apiPass = apiPass
        self.api_url = 'https://payeer.com/ajax/api/api.php'
        self.auth_data = {'account': self.account, 'apiId': self.apiId, 'apiPass': self.apiPass}

    def request(self, **kwargs):
        """The main request method for Payeer API"""
        data = self.auth_data
        if kwargs:
            data.update(kwargs)
        resp = requests.post(url=self.api_url, data=data).json()
        error = resp.get('errors')
        if error:
            raise PayeerAPIException(error)
        else:
            return resp

    def get_balance(self):

        return self.request(action='balance')['balance']

    def get_exchange_rate(self, output='N'):

        return self.request(action='getExchangeRate', output=output)['rate']



if __name__ == "__main__":
    currency = Currency()
    currency.mainloop()
