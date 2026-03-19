from typing import Dict

from xterm_craft_workshop.currency import Currency
from xterm_craft_workshop.missing_exchange_rate_error import MissingExchangeRateError
from xterm_craft_workshop.money import Money


class Bank:

    def __init__(self, pivot: Currency = None) -> None:
        self.pivot = pivot
        self._exchange_rate = {} 

    @staticmethod
    def create(currency1: Currency, currency2: Currency, rate: float) -> "Bank":
        bank = Bank({})
        bank.addExchangeRate(currency1, currency2, rate)

        return bank

    def addExchangeRate(
        self, from_currency: Currency, to_currency: Currency, rate: float
    ) -> None:
        self._exchange_rate[f"{from_currency.value}->{to_currency.value}"] = rate

    def convertMoney_old(self, money: "Money", to_currency: Currency) -> "Money":
        if not self.needExchangeRate(money.currency, to_currency):
            return money
        if self.hasExchangeRate(money.currency, to_currency):
            rate = self._exchange_rate[f"{money.currency.value}->{to_currency.value}"]
            return Money.of(money.amount * rate, to_currency)
        raise MissingExchangeRateError(money.currency, to_currency)
    
    def convertMoney(self, money: "Money", to_currency: Currency) -> "Money":
        from_currency = money.currency

        # 1. même devise
        if not self.needExchangeRate(from_currency, to_currency):
            return money

        # 2. direct rate
        if self.hasExchangeRate(from_currency, to_currency):
            rate = self._exchange_rate[f"{from_currency.value}->{to_currency.value}"]
            return Money.of(money.amount * rate, to_currency)
        
        # 2.5 inverse rate 
        if self.hasExchangeRate(to_currency, from_currency):
            rate = self._exchange_rate[f"{to_currency.value}->{from_currency.value}"]
            return Money.of(money.amount / rate, to_currency)

        # 3. pivot logic 
        if self.pivot is not None:
            # from -> pivot
            if not self.hasExchangeRate(from_currency, self.pivot):
                raise MissingExchangeRateError(from_currency, self.pivot)

            rate1 = self._exchange_rate[f"{from_currency.value}->{self.pivot.value}"]
            intermediate_amount = money.amount * rate1

            # pivot -> to
            if not self.hasExchangeRate(self.pivot, to_currency):
                raise MissingExchangeRateError(self.pivot, to_currency)

            rate2 = self._exchange_rate[f"{self.pivot.value}->{to_currency.value}"]
            final_amount = intermediate_amount * rate2

            return Money.of(final_amount, to_currency)

        # 4. fallback
        raise MissingExchangeRateError(from_currency, to_currency)

    def needExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return from_currency.value != to_currency.value

    def hasExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return f"{from_currency.value}->{to_currency.value}" in self._exchange_rate
    
    def setPivotCurrency(self, pivot: Currency) -> None:
        if not isinstance(pivot, Currency):
            raise ValueError("Invalid currency")
        if self.pivot is not None :
            raise ValueError("Pivot currency is already set")   
        self.pivot = pivot
        
    
