class Account:
    def __init__(self, name, balance, transaction_fee):
        self.name = name
        self.balance = balance
        self.holdings = {}
        self.transaction_fee = transaction_fee # ex. 0.05

    def buy(self, quote, price):
        shares = 0
        print("Account({}) bought {} shares of {}".format(self.name, shares, quote))
        pass

    def sell(self, quote, price):
        shares = 0
        print("Account({}) sold {} shares of {}".format(self.name, shares, quote))
        pass
