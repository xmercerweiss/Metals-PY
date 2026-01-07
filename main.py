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
USD_NAME = "dollars"
COMMENT_SYM = "#"
DWT_SYM = "dwt"
OZ_SYM = "oz"

BANNER_EXT = 0
PRICE_HEADER = f"{'METAL':<10} {'PRICE':>9} {'METAL/GOLD':>11}"
PORTFOLIO_HEADER = f"{'CURRENCY':<10} {'WEIGHT':<9} {'VALUE':>11}"
BANNER = "*" * (len(PRICE_HEADER) + BANNER_EXT)
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
        try:
            portfolio = collect_portfolio(sys.argv[1])
            display_portfolio(prices, portfolio)
        except:
            print(FILE_ERR_MSG)


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(1)


def collect_portfolio(path):
    out = {}
    with open(path, "r") as file:
        for line in file.readlines():
            if len(line.strip()) > 0 and not line.startswith(COMMENT_SYM):
                name, weight = line.lower().strip().split(CONF_SEP)
                out[name] = int(weight)
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
    print(PORTFOLIO_HEADER)
    for name, weight in portfolio.items():
        if weight <= 0:
            continue
        elif name == USD_NAME:
            total_value += weight
            print(PORTFOLIO_FMT.format(
                name.title(),
                "N/A",
                weight
            ))
        elif name in prices:
            price = prices[name]
            total_weight += weight
            value = (price * weight) / 2000
            total_value += value
            print(PORTFOLIO_FMT.format(
                name.title(),
                render_pennyweight(weight),
                value
            ))
    print(BANNER)
    print(PORTFOLIO_FMT.format(
        "Total",
        render_pennyweight(total_weight),
        total_value
    ))


def display_prices(prices):
    au_price = prices[AU_NAME]
    print(PRICE_HEADER)
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

