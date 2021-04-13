class Strategy:
    def __init__(self):
        self.history = []
        self.sum = 0
        self.charts = []

    def on_data(self, info):

        close_price = info["c"]
        self.history.append(close_price)
        self.sum += close_price

        if close_price > self.sum/len(self.history)*1:
            return -1
        elif close_price < self.sum/len(self.history)*0.9:
            return 1

        return 0
