from typing import List, Tuple
from .currency import Currency
from .bank import Bank


class Portfolio:
    def __init__(self) -> None:
        self._moneys: List[Tuple[float, Currency]] = []

    def add(self, amount: float, currency: Currency) -> None:
        self._moneys.append((amount, currency))

    def evaluate(self, bank: Bank, currency: Currency) -> float:
        total = 0.0
        for amount, money_currency in self._moneys:
            total += bank.convert(amount, money_currency, currency)
        return total
