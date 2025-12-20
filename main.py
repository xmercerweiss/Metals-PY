from urllib.request import urlopen

import json
import sys


SOURCE = "https://www.kitco.com/api/kitco-xml/precious-metals"

URL_ERR_MSG = "Couldn't connect to price source, double-check URL and connection."
FILE_ERR_MSG = "Could not display portfolio."

NAME_KEY = "commodity"
BID_KEY = "lastBid"
PRICE_KEY = "bidVal"
CONF_SEP = "="
AU_NAME = "gold"
DWT_SYM = "dwt"
OZ_SYM = "oz"

BANNER_EXT = 0
HEADER = f"{'METAL':<10} {'PRICE':>9} {'METAL/GOLD':>11}"
BANNER = "*" * (len(HEADER) + BANNER_EXT)
PRICE_FMT = "{:<10} ${:8.2f} {:11.2f}"
PORTFOLIO_FMT = "{:<10} {:<11} ${:8.2f}"


def main():
    try:
        response = urlopen(SOURCE)
        data = json.loads(response.read())["data"]
    except:
        error(URL_ERR_MSG)
    prices = collect_prices(data)
    display_prices(prices)
    if (len(sys.argv) > 1):
        #try:
        portfolio = collect_portfolio(sys.argv[1])
        display_portfolio(prices, portfolio)
        #except:
         #   print(FILE_ERR_MSG)


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(1)


def collect_portfolio(path):
    out = {}
    with open(path, "r") as file:
        for line in file.readlines():
            name, value = line.lower().strip().split(CONF_SEP)
            out[name] = int(value)
    return out


def collect_prices(data):
    return {get_metal_name(m) : get_metal_price(m) for m in data}


def get_metal_name(metal):
    return metal[NAME_KEY].lower()


def get_metal_price(metal):
    return int(metal[BID_KEY][PRICE_KEY] * 100)


def display_portfolio(prices, portfolio):
    total_value = 0
    total_weight = 0
    print(BANNER)
    for name, value in portfolio.items():
        if name in prices and value > 0:
            price = prices[name]
            total_weight += value
            dollar_value = (price * value) / 2000
            total_value += dollar_value
            print(PORTFOLIO_FMT.format(
                name.title(),
                render_pennyweight(value),
                dollar_value
            ))
    print(PORTFOLIO_FMT.format(
        "Total",
        render_pennyweight(total_weight),
        total_value
    ))


def display_prices(prices):
    au_price = prices[AU_NAME]
    print(HEADER)
    for name, price in prices.items():
        print(PRICE_FMT.format(
            name.title(),
            price / 100,
            au_price / price
        ))


def render_pennyweight(dwt):
    if dwt == 0 or dwt % 20 == 0:
        return f"{dwt // 20}{OZ_SYM}"
    elif dwt < 20:
        return f"{dwt}{DWT_SYM}"
    else:
        return f"{dwt // 20}{OZ_SYM} {dwt % 20}{DWT_SYM}"
    

if __name__ == "__main__":
    main()

