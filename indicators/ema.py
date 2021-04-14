from indicators import sma


class Indicator:
    def __init__(self, periods):
        self.history = []
        self.sum = 0
        self.periods = periods
        self.prev_ema = 0
        self.smoothing = 2

        self.sma_calc = sma.Indicator(periods=periods)

    def get_ema(self):
        price = self.history[-1]
        self.sum += price
        if len(self.history) > self.periods:
            self.sum -= self.history[-self.periods]

        return (price * self.smoothing/(1+self.periods)) + self.prev_ema * (1 - self.smoothing/(1+self.periods))

    def on_data(self, price):
        self.history.append(price)

        if len(self.history) < self.periods+1:
            sma_ = self.sma_calc.on_data(price)
            self.prev_ema = sma_
            return sma_

        ema = self.get_ema()
        self.prev_ema = ema
        return ema
