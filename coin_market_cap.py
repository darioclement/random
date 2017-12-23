import os
import sys
import threading
import time
from coinmarketcap import Market
from crypto_data import ContectManager

trial = ContectManager()
coinmarketcap = Market()
coinmarketcap.ticker('bitcoin', limit=3, convert='CAD')
coin_list = ['bitcoin', 'ethereum', 'bitcoin-cash', 'litecoin']

BUFFER_SIZE = 2


def worker(Market, buf, coin):
    """thread worker function"""
    coin_market_cap = Market()
    while True:
        with trial: buf.append(coin_market_cap.ticker(coin, limit=3, convert='CAD'))
        time.sleep(10)


class RingBuffer:
    """ring buffer to hold raw data"""
    def __init__(self, size):
        self.data = [None for _ in range(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data


threads = list()
buffers = list()
for coin in coin_list:
    buf = RingBuffer(BUFFER_SIZE)
    buffers.append(buf)
    t = threading.Thread(target=worker, args=(Market, buf, coin))
    threads.append(t)

for thread in threads:
    thread.start()


first_run = True
while True:
    for buffer in enumerate(buffers):
        if buffer[1].data[-1] is not None:
            print(list(filter(lambda x: x is not None, buffer[1].data))[-1][0])

    time.sleep(10)


# Data structure from coin market cap:
#
# ticker
# dict:
#     id
#     name
#     symbol
#     rank
#     price_usd
#     price_btc
#     24h_volume_usd
#     market_cap_usd
#     available_supply
#     total_supply
#     max_supply
#     percent_change_1h
#     percent_change_24h
#     percent_change_7d
#     last_updated
#     price_cad
#     24h_volume_cad
#     market_cap_cad
#     cached
