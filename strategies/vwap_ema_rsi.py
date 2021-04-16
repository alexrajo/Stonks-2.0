from indicators import vwap, rsi, ema


class Strategy:
    def __init__(self):
        self.history = []
        self.indicators = {
            "vwap": vwap.Indicator(periods=50),
            "rsi": rsi.Indicator(periods=14),
            "ema": ema.Indicator(periods=600)
        }

    def on_data(self, info):
        self.history.append(info["c"])

        decision = 0
        return {"decision": decision}
