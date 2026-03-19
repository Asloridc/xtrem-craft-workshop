from xterm_craft_workshop.bank import Bank


class BankBuilder:
    def __init__(self):
        self.rates = []
        self.pivot = None

    def with_pivot(self, pivot):
        self.pivot = pivot
        return self

    def with_rate(self, from_currency, to_currency, rate):
        self.rates.append((from_currency, to_currency, rate))
        return self

    def build(self):
        if self.pivot is None:
            raise ValueError("Pivot must be defined")

        bank = Bank(self.pivot)

        for from_currency, to_currency, rate in self.rates:
            bank.addExchangeRate(from_currency, to_currency, rate)

        return bank
