from indicators import ema, rsi


class Strategy:
    def __init__(self):
        self.trend = "neutral"
        self.indicators = {
            "ema": ema.Indicator(periods=200),
            "rsi": rsi.Indicator(periods=14)
        }

    def on_data(self, info):

        close_price = info["c"]
        ema_ = self.indicators["ema"].on_data(price=close_price)
        rsi_ = self.indicators["rsi"].on_data(price=close_price)

        decision = 0

        if close_price > ema_*1.05:
            self.trend = "up"
        else:
            self.trend = "down"

        if self.trend == "up" and rsi_ > 70:
            decision = -1
        elif self.trend == "up" and rsi_ < 50:
            decision = 1

        return {"decision": decision, "charts": ["200 ema", ema_, False, "14 rsi", rsi_, True]}
