import requests


def fetch_data():
    url = "https://www.modularfinance.se/static/files/puzzles/index-trader.json"
    data = requests.get(url=url).json()
    return data


def find_trades():

    data = fetch_data()["data"]

    # save first index (blob) as highest and lowest, for both current interval and total
    curr_high = curr_low = tot_high = tot_low = data[len(data)-1]
    curr_rev = tot_rev = curr_high['high'] - curr_low['low']

    # iterate all indexes (blobs), compare each blob to curr_low and curr_high.
    # if a new low is found, a new interval starts and both curr_low and curr_high will be updated.
    # if a new high is found, curr_high will be updated
    # if a new high or low is found, curr_rev will be updated and if higher than tot_rev --> tot_low and tot_high will be updated accordingly
    for blob in reversed(data):
        if blob["low"] < curr_low["low"]:
            # new interval
            curr_high = curr_low = blob
            curr_rev = curr_high['high'] - curr_low['low']

        if blob["high"] > curr_high['high']:
            curr_high = blob
            curr_rev = curr_high['high'] - curr_low['low']

        if curr_rev > tot_rev:
            # new total highest revenue found
            tot_low = curr_low
            tot_high = curr_high
            tot_rev = curr_rev

    highest_price = tot_high['high']
    lowest_price = tot_low['low']

    print(f"highest price: {highest_price}, date: {tot_high['quote_date']}")
    print(f"lowest price: {lowest_price}, date: {tot_low['quote_date']}")
    print(f"Profit: {highest_price-lowest_price}")

find_trades()
