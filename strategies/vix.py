from indicators import vix


class Strategy:
    def __init__(self):
        self.indicator = vix.Indicator()
        self.buy_threshold = 30
        self.sell_threshold = 20

    def on_data(self, info):
        vix_ = self.indicator.on_data()

        decision = 0

        if vix_["c"] >= self.buy_threshold:
            decision = 1
        elif vix_["c"] < self.sell_threshold:
            decision = -1

        return {"decision": decision, "charts": ["vix", vix_["c"]], "separated": True}
