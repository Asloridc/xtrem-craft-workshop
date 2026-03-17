
from xterm_craft_workshop.bank import Bank
from xterm_craft_workshop.currency import Currency
from xterm_craft_workshop.missing_exchange_rate_error import MissingExchangeRateError
from xterm_craft_workshop.money import Money


class TestBank:
    def test_givenEuroAmount_WhenConvertToUsd_ThenReturnsUsdAmount(self):
        # GIVEN
        from_currency = Currency.EUR
        to_currency = Currency.USD
        rate = 1.2
        bank = Bank.create(from_currency, to_currency, rate)
        amount = 10
        expected = Money.of(12, Currency.USD)
        # WHEN
        result = bank.convertMoney(Money.of(amount, from_currency), to_currency)
        # THEN
        assert result == expected

    def test_givenEuroAmount_WhenConvertToSameCurrency_ThenReturnsSameAmount(self):
        # GIVEN
        from_currency = Currency.EUR
        to_currency = Currency.EUR
        rate = 1
        bank = Bank.create(from_currency, to_currency, rate)
        amount = 10
        expected = Money.of(10, Currency.EUR)
        # WHEN
        result = bank.convertMoney(Money.of(amount, from_currency), to_currency)

        # THEN
        assert result == expected

    def test_givenEuroAmount_WhenConvertWithMissingExchangeRate_ThenThrowsException(
        self,
    ):
        # GIVEN
        from_currency = Currency.EUR
        to_currency = Currency.KRW
        bank = Bank()
        amount = 10
        # WHEN
        try:
            bank.convertMoney(Money.of(amount, from_currency), to_currency)
            # THEN
            assert False
        except MissingExchangeRateError:
            assert True

    def test_givenEuroAmount_WhenConvertWithDifferentExchangeRate_ThenReturnsDifFloats(
        self,
    ):

        # Given

        bank: Bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        assert bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD) == Money.of(
            12, Currency.USD
        )

        bank.addExchangeRate(Currency.EUR, Currency.USD, 1.3)

        assert bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD) == Money.of(
            13, Currency.USD
        )
