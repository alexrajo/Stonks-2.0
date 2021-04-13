from alpha_vantage import *
from config import *
import requests
import threading

import strategies.golden_cross as gc

class Paperbot:
    def __init__(self, symbol, strategy):
        self.LONG_PARAMS = LONG_PARAMS
        self.LONG_PARAMS["symbol"] = symbol or "EQNR"
        self.interval = 150

        self.calc = strategy.Strategy()
        self.setup()

    def setup(self):

        response = requests.get(AV_REQUEST_URL, LONG_PARAMS)
        formatted_response = response.json()
        response_body = formatted_response["Time Series (5min)"]

        for t in response_body:
            content = response_body[t]
            info = {
                "o": float(content["1. open"]),
                "h": float(content["2. high"]),
                "l": float(content["3. low"]),
                "c": float(content["4. close"]),
                "v": int(content["5. volume"])
            }
            self.calc.on_data(info=info)

        self.run_tick()

    def run_tick(self):
        threading.Timer(self.interval, self.run_tick).start()
        self.do_trading()

    def do_trading(self):
        response = requests.get(AV_REQUEST_URL, CURRENT_PRICE_PARAMS)
        formatted_response = response.json()
        content = formatted_response["Global Quote"]
        info = {
            "o": float(content["02. open"]),
            "h": float(content["03. high"]),
            "l": float(content["04. low"]),
            "c": float(content["05. price"]),
            "v": float(content["06. volume"]),
        }
        decision = self.calc.on_data(info=info)
        print("Price: {}, Decision: {}".format(info["c"], decision))


p = Paperbot(symbol="EQNR", strategy=gc)
