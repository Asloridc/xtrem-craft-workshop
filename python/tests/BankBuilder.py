from xterm_craft_workshop.bank import Bank


class BankBuilder:
    def __init__(self):
        self.rates = []

    def with_rate(self, from_currency, to_currency, rate):
        self.rates.append((from_currency, to_currency, rate))
        return self

    def build(self):
        bank = Bank()
        for from_currency, to_currency, rate in self.rates:
            bank.addExchangeRate(from_currency, to_currency, rate)
        return bank
