import matplotlib.pyplot as plotter
import quandl
import numpy as np
from config import *

# strategies
from strategies import test, golden_cross, rsi

quandl.ApiConfig.api_key = QUANDL_API_KEY

transaction_fee = 0.0015
vix = "CHRIS/CBOE_VX1"

class Backtester:
    def __init__(self):
        self.capital = 0
        self.holding = 0
        self.portfolio = 0
        self.strategies = {
            "test": [test],
            "golden_cross": [golden_cross],
            "rsi": [rsi],
            "rsi/golden_cross": [rsi, golden_cross]
        }

    def get_moving_average(self, periods, history):
        ma = []
        t = 0
        sum = 0
        for b in history:
            t += 1
            sum += b
            if t > periods:
                sum -= history[t-periods]

            div = min(t, periods)
            ma.append(sum/div)

        return ma

    def run_test(self, stock, strategy, capital):
        self.capital = capital
        self.holding = 0
        self.portfolio = self.capital
        data = quandl.get(stock, returns="numpy", collapse="daily")

        x = []
        closing_prices = []
        actions = []
        portfolio_history = []
        calcs = []
        for s in self.strategies[strategy]:
            calcs.append(s.Strategy())

        def set_portfolio_value(price):
            self.portfolio = self.capital + self.holding*price
            portfolio_history.append(self.portfolio)

        def buy(price):
            if self.capital-price*transaction_fee > price:
                order_size = int(self.capital/price)
                self.capital -= order_size*price + price*transaction_fee
                self.holding += order_size
                return True

            return False

        def sell(price):
            if self.holding > 0:
                self.capital += self.holding*price - price*transaction_fee
                self.holding = 0
                return True

            return False

        for bar in data:
            info = {
                "o": bar[1],
                "h": bar[2],
                "l": bar[3],
                "c": bar[4],
                "v": bar[5]
            }
            t = len(x)+1
            x.append(t)
            closing_prices.append(info["c"])

            decision = 0
            for calc in calcs:
                d = calc.on_data(info=info)
                decision += d

            color = (decision == 1) and "green" or "red"

            if decision == 1:
                completed = buy(info["c"])
                if completed:
                    actions.append({"t": t, "c": "green"})
            elif decision == -1:
                completed = sell(info["c"])
                if completed:
                    actions.append({"t": t, "c": "red"})

            set_portfolio_value(info["c"])

        figure, plots = plotter.subplots(2)
        plots[0].plot(x, closing_prices)
        plots[1].plot(x, portfolio_history)

        for calc in calcs:
            for chart_type in calc.charts:
                if chart_type[0] == "ma":
                    for i in range(1, len(chart_type)):
                        plots[0].plot(x, self.get_moving_average(chart_type[i], closing_prices))

        plots[0].set_title("Closing price history ({})".format(stock))
        plots[1].set_title("Portfolio value history")

        for action in actions:
            plots[0].axvline(action["t"], 0, 1, color=action["c"])

        plotter.xlabel("Days")
        plots[0].set_ylabel("Closing price")
        plots[1].set_ylabel("Value")

        # plotter.figure(num="{} BACKTEST".format(stock))
        plotter.show()

        results = {
            "percent_change": (portfolio_history[0] > 0) and int((portfolio_history[-1]/portfolio_history[0]-1)*1000)/10 or 0,
            "start": int(portfolio_history[0]*10)/10,
            "end": int(portfolio_history[-1]*10)/10
        }
        return results
