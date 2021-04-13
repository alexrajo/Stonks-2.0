from indicators import sma


class Strategy:
    def __init__(self):
        self.indicators = {
            "50": sma.Indicator(periods=50),
            "200": sma.Indicator(periods=200)
        }
        self.prev_ma = {
            "50": 0,
            "200": 0
        }
        self.charts = [
            ["ma", 50, 200]
        ]

    def on_data(self, info):

        close_price = info["c"]
        ma_50 = self.indicators["50"].on_data(close_price)
        ma_200 = self.indicators["200"].on_data(close_price)

        decision = 0

        if ma_50 < ma_200 and self.prev_ma["50"] >= self.prev_ma["200"]:
            decision = 1
        elif ma_50 > ma_200 and self.prev_ma["50"] <= self.prev_ma["50"]:
            decision = -1

        self.prev_ma["50"] = ma_50
        self.prev_ma["200"] = ma_200
        return decision
