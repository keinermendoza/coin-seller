from typing import List, Dict, Tuple, Callable
from decimal import getcontext as decimal_getcontext, Decimal, ROUND_DOWN
from django.core.exceptions import ValidationError
import requests
from copy import copy
from concurrent.futures import ThreadPoolExecutor

# for know about decimal.getcontext
# https://stackoverflow.com/questions/8595973/truncate-to-three-decimals-in-python
# https://docs.python.org/3/library/decimal.html#context-objects


HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "content-type": "application/json",
    "Host": "p2p.binance.com",
    "Origin": "https://p2p.binance.com",
    "Pragma": "no-cache",
    "TE": "Trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
}

SEARCH_API = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"


# https://stackoverflow.com/questions/67793326/api-binance-p2p-i-only-access-a-part-only-the-buy-and-not-all-of-it-buy-and-s
# https://github.com/n4t1412dev/binance-p2p-api/blob/main/src/BinanceApi/Binance.php

BASIC_PAYLOAD = {
    # "fiat": "VES",
    "page": 1,
    "rows": 20,
    # "transAmount": 5000,
    # "tradeType": "SELL",
    # "asset": "USDT",
    "countries": [],
    "proMerchantAds": False,
    "shieldMerchantAds": False,
    "filterType": "all",
    "periods": [],
    "additionalKycVerifyFilter": 0,
    "publisherType": "merchant",
    "payTypes": [],
    "classifies": ["mass", "profession", "fiat_trade"],
}


def get_listing_for_currency(
    currency: str, trade_type: str = "SELL", asset: str = "USDT", **kwargs
) -> Dict[str, List[Decimal]]:
    """make request to p2p api and returns price list
    extra arguments are pass to the payload
    """

    payload = copy(BASIC_PAYLOAD)
    payload.update(
        {"tradeType": trade_type, "fiat": currency, "asset": asset, **kwargs}
    )

    response = requests.post(SEARCH_API, headers=HEADERS, json=payload)
    data = response.json()
    return data


def extract_listing_data(
    data: Dict,
    keys_data_to_extract: List[str] = [
        "price",
        "payTimeLimit",
        "minSingleTransAmount",
        "maxSingleTransAmount",
    ],
    get_trade_methods_list: bool = True,
) -> Dict:
    "takes a single dict a returns the selected indicated by keys_data_to_extract"

    listings_key = "adv"
    listings_dict = {}

    for key in keys_data_to_extract:
        listings_dict[key] = data[listings_key][key]

    if get_trade_methods_list:
        listings_dict["tradeMethods"] = [
            method["payType"] for method in data[listings_key]["tradeMethods"]
        ]
    return listings_dict


def extract_publisher_data(
    data: Dict, keys_data_to_extract: List[str] = ["nickName", "positiveRate"]
) -> Dict:
    "takes a single dict a returns the selected indicated by keys_data_to_extract"
    publishers_key = "advertiser"
    publisher_dict = {}

    for key in keys_data_to_extract:
        publisher_dict[key] = data[publishers_key][key]
    return publisher_dict


def extract_relevant_data(data: Dict, **kwargs):
    relevant_data = []
    for item in data["data"]:
        item_data: Dict = extract_listing_data(item, **kwargs) | extract_publisher_data(
            item, **kwargs
        )
        relevant_data.append(item_data)

    return relevant_data
