from typing import Dict

from xterm_craft_workshop.currency import Currency
from xterm_craft_workshop.missing_exchange_rate_error import MissingExchangeRateError
from xterm_craft_workshop.money import Money


class Bank:
    _exchange_rate: Dict[str, float] = {}

    def __init__(self, exchange_rate={}) -> None:
        self._exchange_rate = exchange_rate

    @staticmethod
    def create(currency1: Currency, currency2: Currency, rate: float) -> "Bank":
        bank = Bank({})
        bank.addExchangeRate(currency1, currency2, rate)

        return bank

    def addExchangeRate(
        self, from_currency: Currency, to_currency: Currency, rate: float
    ) -> None:
        self._exchange_rate[f"{from_currency.value}->{to_currency.value}"] = rate

    def convertMoney(self, money: "Money", to_currency: Currency) -> "Money":
        if not self.needExchangeRate(money.currency, to_currency):
            return money
        if self.hasExchangeRate(money.currency, to_currency):
            rate = self._exchange_rate[f"{money.currency.value}->{to_currency.value}"]
            return Money.of(money.amount * rate, to_currency)
        raise MissingExchangeRateError(money.currency, to_currency)

    def needExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return from_currency.value != to_currency.value

    def hasExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return f"{from_currency.value}->{to_currency.value}" in self._exchange_rate
