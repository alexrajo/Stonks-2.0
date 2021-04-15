import quandl
ticker = "CHRIS/CBOE_VX1"


class Indicator:
    def __init__(self):
        data = quandl.get(ticker, returns="numpy", collapse="daily")
        self.index = -1
        self.vix_history = []
        for bar in data:
            info = {
                "o": bar[1],
                "h": bar[2],
                "l": bar[3],
                "c": bar[4],
                "v": bar[5]
            }
            self.vix_history.append(info)

    def on_data(self):
        self.index += 1
        return self.vix_history[self.index]
