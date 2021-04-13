def calculate_rsi(avg_gain, avg_loss):
    avg_gain = avg_gain != 0 and avg_gain or 1
    avg_loss = avg_loss != 0 and avg_loss or 1

    rsi = 100 - (100 / (1 + avg_gain / avg_loss))
    return rsi


class Indicator:
    def __init__(self, periods):
        self.history = []
        self.gain_sum = 0
        self.loss_sum = 0
        self.periods = periods

        self.gain_history = []
        self.loss_history = []

    def on_data(self, price):

        change_percent = len(self.history) > 0 and (price/self.history[-1]-1)*100 or 0

        if change_percent > 0:
            self.gain_sum += abs(change_percent)
            self.gain_history.append(abs(change_percent))
            self.loss_history.append(0)
        else:
            self.loss_sum += abs(change_percent)
            self.loss_history.append(abs(change_percent))
            self.gain_history.append(0)

        if len(self.history) > 13:
            self.gain_sum -= self.gain_history[-self.periods]
            self.loss_sum -= self.loss_history[-self.periods]

        t = max(1, min(len(self.history), self.periods))
        self.history.append(price)

        rsi = calculate_rsi(self.gain_sum/t, self.loss_sum/t)
        return rsi
