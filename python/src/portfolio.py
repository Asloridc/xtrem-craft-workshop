from typing import List, Tuple

from .bank import Bank
from .currency import Currency
from .money import Money


class Portfolio:
    def __init__(self) -> None:
        self._moneys_old: List[Tuple[float, Currency]] = []
        self._moneys: List[Money] = []

    def add(self, amount: float, currency: Currency) -> None:
        self._moneys.append(Money.of(amount, currency))

    def evaluate(self, bank: Bank, currency: Currency) -> Money:
        total = Money.of(0.0, currency)
        for money in self._moneys:
            total += bank.convertMoney(money, currency)
        return total
