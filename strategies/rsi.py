from indicators import rsi


class Strategy:
    def __init__(self):
        self.indicator = rsi.Indicator(periods=14)

        self.overbought_threshold = 70
        self.oversold_threshold = 30

        self.charts = [
            ["rsi"]
        ]

    def on_data(self, info):

        close_price = info["c"]
        rsi = self.indicator.on_data(close_price)

        if rsi >= self.overbought_threshold:
            return -1
        elif rsi <= self.oversold_threshold:
            return 1

        return 0
