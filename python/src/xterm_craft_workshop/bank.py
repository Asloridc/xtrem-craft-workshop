from xterm_craft_workshop.currency import Currency
from xterm_craft_workshop.missing_exchange_rate_error import MissingExchangeRateError
from xterm_craft_workshop.money import Money


class Bank:
    def __init__(self, pivot: Currency) -> None:
        if not isinstance(pivot, Currency):
            raise ValueError("Invalid pivot currency")

        self.pivot = pivot
        self._exchange_rate = {}

    @staticmethod
    def create(currency1: Currency, currency2: Currency, rate: float) -> "Bank":
        bank = Bank(Currency.USD)  # Set a default pivot currency
        bank.addExchangeRate(currency1, currency2, rate)
        return bank

    def addExchangeRate(
        self, from_currency: Currency, to_currency: Currency, rate: float
    ) -> None:
        if rate <= 0:
            raise ValueError("Exchange rate must be positive")

        key = f"{from_currency.value}->{to_currency.value}"
        self._exchange_rate[key] = rate

    def convertMoney(self, money: "Money", to_currency: Currency) -> "Money":
        from_currency = money.currency

        # 1. même devise
        if from_currency == to_currency:
            return money

        # 2. direct
        if self.hasExchangeRate(from_currency, to_currency):
            rate = self._exchange_rate[f"{from_currency.value}->{to_currency.value}"]
            return Money.of(money.amount * rate, to_currency)

        # 3. inverse
        if self.hasExchangeRate(to_currency, from_currency):
            rate = self._exchange_rate[f"{to_currency.value}->{from_currency.value}"]
            return Money.of(money.amount / rate, to_currency)

        # 4. pivot obligatoire
        if self.pivot is None:
            raise MissingExchangeRateError(from_currency, to_currency)

        return self._convert_via_pivot(money, to_currency)

    def _convert_via_pivot(self, money: "Money", to_currency: Currency) -> "Money":
        from_currency = money.currency

        # from pivot
        if not self.hasExchangeRate(from_currency, self.pivot):
            raise MissingExchangeRateError(from_currency, self.pivot)

        rate1 = self._exchange_rate[f"{from_currency.value}->{self.pivot.value}"]
        intermediate_amount = money.amount * rate1

        # pivot to
        if not self.hasExchangeRate(self.pivot, to_currency):
            raise MissingExchangeRateError(self.pivot, to_currency)

        rate2 = self._exchange_rate[f"{self.pivot.value}->{to_currency.value}"]
        final_amount = intermediate_amount * rate2

        return Money.of(final_amount, to_currency)

    def hasExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        return f"{from_currency.value}->{to_currency.value}" in self._exchange_rate

    def setPivotCurrency(self, pivot: Currency) -> None:
        if not isinstance(pivot, Currency):
            raise ValueError("Invalid currency")

        if pivot is None:
            raise ValueError("Pivot cannot be null")

        if self.pivot is not None:
            raise ValueError("Pivot currency is already set")

        self.pivot = pivot
