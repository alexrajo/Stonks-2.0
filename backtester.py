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
        indicator_charts = {}
        for s in self.strategies[strategy]:
            calc = s.Strategy()
            calcs.append(calc)

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
                response = calc.on_data(info=info)
                d = response["decision"]
                decision += d

                charts_ = response.get("charts") or []
                separated = response.get("separated") or False
                for ci in range(len(charts_)):
                    if ci % 2 != 0:
                        continue

                    if indicator_charts.get(charts_[ci]) is None:
                        indicator_charts[charts_[ci]] = {"data": [], "separated": separated}

                    indicator_charts[charts_[ci]]["data"].append(charts_[ci+1])

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

        indicator_subplots = 0
        for chart_name in indicator_charts:
            if indicator_charts[chart_name]["separated"]:
                indicator_subplots += 1

        figure, plots = plotter.subplots(2+indicator_subplots)
        plots[0].plot(x, closing_prices)
        plots[1].plot(x, portfolio_history)

        plots[0].set_title("Closing price history ({})".format(stock))
        plots[1].set_title("Portfolio value history")

        current_extraplot = 2
        for chart_name in indicator_charts:
            chart = indicator_charts[chart_name]
            if chart["separated"]:
                plots[current_extraplot].plot(x, chart["data"])
                plots[current_extraplot].set_title(chart_name)
            else:
                plots[0].plot(x, chart["data"])

        for action in actions:
            plots[0].axvline(action["t"], 0, 1, color=action["c"])

        plotter.xlabel("Days")
        plots[0].set_ylabel("Closing price")
        plots[1].set_ylabel("Value")

        plotter.subplots_adjust(hspace=0.4+indicator_subplots*0.4)

        # plotter.figure(num="{} BACKTEST".format(stock))
        plotter.show()

        results = {
            "percent_change": (portfolio_history[0] > 0) and int((portfolio_history[-1]/portfolio_history[0]-1)*1000)/10 or 0,
            "start": int(portfolio_history[0]*10)/10,
            "end": int(portfolio_history[-1]*10)/10
        }
        return results
