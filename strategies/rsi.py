from indicators import rsi


class Strategy:
    def __init__(self):
        self.indicator = rsi.Indicator(periods=14)

        self.overbought_threshold = 70
        self.oversold_threshold = 30

    def on_data(self, info):

        close_price = info["c"]
        rsi_ = self.indicator.on_data(close_price)

        decision = 0

        if rsi_ >= self.overbought_threshold:
            decision = -1
        elif rsi_ <= self.oversold_threshold:
            decision = 1

        return {"decision": decision, "charts": ["rsi", rsi_, True]}
