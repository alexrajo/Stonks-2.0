class Indicator:
    def __init__(self, periods):
        self.history = []
        self.sum = 0
        self.periods = periods

    def get_moving_average(self):
        self.sum += self.history[-1]
        if len(self.history) > self.periods:
            self.sum -= self.history[-self.periods]

        return self.sum/min(self.periods, len(self.history))

    def on_data(self, price):
        self.history.append(price)
        return self.get_moving_average()
