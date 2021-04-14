class Strategy:
    def __init__(self):
        self.history = []
        self.sum = 0
        self.charts = []

    def on_data(self, info):

        close_price = info["c"]
        self.history.append(close_price)
        self.sum += close_price

        decision = 0

        if close_price > self.sum/len(self.history)*1:
            decision = -1
        elif close_price < self.sum/len(self.history)*0.9:
            decision = 1

        return {"decision": decision}
