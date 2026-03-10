from typing import Dict
from .currency import Currency
from .missing_exchange_rate_error import MissingExchangeRateError


class Bank:
    _exchange_rate: Dict[str, float] = {}

    def __init__(self, exchange_rate = {}) -> None:
        self._exchange_rate = exchange_rate

    @staticmethod
    def create(currency1: Currency, currency2: Currency, rate: float) -> "Bank":
        bank = Bank({})
        bank.addExchangeRate(currency1, currency2, rate)

        return bank
    
    def addExchangeRate(self, from_currency: Currency, to_currency: Currency, rate: float) -> None:
        self._exchange_rate[f'{from_currency.value}->{to_currency.value}'] = rate

    def convert(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)
    
    def needExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return from_currency.value != to_currency.value

    def hasExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return f'{from_currency.value}->{to_currency.value}' in self._exchange_rate