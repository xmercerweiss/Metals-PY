from urllib.request import urlopen
import json


SOURCE = "https://www.kitco.com/api/kitco-xml/precious-metals"

NAME_KEY = "commodity"
BID_KEY = "lastBid"
PRICE_KEY = "bidVal"

AU_NAME = "gold"

HEADER = f"{'METAL':<10} {'PRICE':>9} {'METAL/GOLD':>11}"
OUTPUT_FMT = "{:<10} ${:8.2f} {:11.2f}"


def main():
    response = urlopen(SOURCE)
    data = json.loads(response.read())["data"]
    prices = collect_prices(data)
    display_prices(prices)


def collect_prices(data):
    return {get_metal_name(m) : get_metal_price(m) for m in data}


def get_metal_name(metal):
    return metal[NAME_KEY].lower()


def get_metal_price(metal):
    return int(metal[BID_KEY][PRICE_KEY] * 100)


def display_prices(prices):
    au_price = prices[AU_NAME]
    print(HEADER)
    for name, price in prices.items():
        print(OUTPUT_FMT.format(
            name.title(),
            price / 100,
            au_price / price
        ))
    

if __name__ == "__main__":
    main()

