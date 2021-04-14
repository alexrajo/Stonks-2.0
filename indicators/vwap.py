class Indicator:
    def __init__(self, periods):
        self.periods = periods
        self.history = []
        self.volume_history = []
        self.sum = 0
        self.volume_sum = 0

    def on_data(self, price, volume):
        self.history.append(price)
        self.volume_history.append(volume)

        self.sum += self.history[-1]
        self.volume_sum += self.volume_history[-1]
        if len(self.history) > self.periods:
            self.sum -= self.history[-self.periods]
            self.volume_sum -= self.volume_history[-self.periods]

        return self.sum*volume/self.volume_sum
