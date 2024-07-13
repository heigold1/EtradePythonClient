"""This Python script provides examples on using the E*TRADE API endpoints"""
from __future__ import print_function
import webbrowser
import json
import logging
import configparser
import sys
import requests
import tkinter as tk
from tkinter import messagebox
import pyperclip
import re

from rauth import OAuth1Service
from logging.handlers import RotatingFileHandler
from accounts.accounts import Accounts
from market.market import Market
from order.order import Order

# loading configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5*1024*1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)


def place_order(session, account, base_url):
    logger.debug("Inside place_order")

    # Grab text from clipboard
    clipboard_text = pyperclip.paste()

    order = Order(session, account, base_url)
    order.place_order(clipboard_text)


def main():


    """Allows user authorization for the sample application with OAuth 1"""

    etrade = OAuth1Service(
        name="etrade",
        consumer_key=config["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret=config["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")

    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"})

    print("\nThe request_token is :" + request_token + " and the request_token_secret is " + request_token_secret)

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a verification code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    webbrowser.open(authorize_url)
    text_code = input("Please accept agreement and enter verification code from browser: ")

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})


    account = {
        'accountId': '151706697',
        'accountIdKey': 'S11DfWByF1AJIO-pGBEw-g',
        'accountMode': 'MARGIN',
        'accountDesc': 'US Stocks',
        'accountName': 'US Stocks',
        'accountType': 'INDIVIDUAL',
        'institutionType': 'BROKERAGE',
        'accountStatus': 'ACTIVE',
        'closedDate': 0,
        'shareWorksAccount': False,
        'fcManagedMssbClosedAccount': False
    }

    base_url = "https://api.etrade.com"

    root = tk.Tk()
    root.title("Place Order")

    place_order_button = tk.Button(root, text="Place Order", command = lambda: place_order(session, account, base_url))
    place_order_button.pack(pady=20)

    root.mainloop()




if __name__ == "__main__":
    main()
