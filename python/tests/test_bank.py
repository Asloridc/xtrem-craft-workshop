from xterm_craft_workshop.bank import Bank
from xterm_craft_workshop.currency import Currency
from xterm_craft_workshop.missing_exchange_rate_error import MissingExchangeRateError
from xterm_craft_workshop.money import Money

from .BankBuilder import BankBuilder


class TestBank:
    #Given EUR->USD rate
    def test_givenEuroAmount_WhenConvertToUsd_ThenReturnsUsdAmount(self):
        # GIVEN
        bank = BankBuilder().with_rate(Currency.EUR, Currency.USD, 1.2).build()

        # WHEN
        result = bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD)

        # THEN
        assert result == Money.of(12, Currency.USD)
    #Given missing EUR->USD rate
    def test_givenEuroAmount_WhenConvertToSameCurrency_ThenReturnsSameAmount(self):
        # GIVEN
        bank = BankBuilder().build()
        amount = 10
        from_currency = Currency.EUR
        to_currency = Currency.EUR

        # WHEN
        result = bank.convertMoney(Money.of(amount, from_currency), to_currency)

        # THEN
        assert result == Money.of(10, Currency.EUR)
    #Given missing EUR->USD rate
    def test_givenEuroAmount_WhenConvertWithMissingExchRate_ThenThrowsException(self):
        # GIVEN
        bank = BankBuilder().build()

        # WHEN / THEN
        try:
            bank.convertMoney(Money.of(10, Currency.EUR), Currency.KRW)
            assert False
        except MissingExchangeRateError:
            assert True
    #Given EUR->USD, pivot USD, missing USD->JPY
    def test_givenEuroAmount_WhenConvertWithDiffExchangeRate_ThenReturnsFloats(self):
        # GIVEN
        bank = (
            BankBuilder()
            .with_rate(Currency.EUR, Currency.USD, 1.2)
            .build()
        )

        # WHEN
        first = bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD)

        # THEN
        assert first == Money.of(12, Currency.USD)

        # WHEN (update rate)
        bank.addExchangeRate(Currency.EUR, Currency.USD, 1.3)

        # THEN
        second = bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD)
        assert second == Money.of(13, Currency.USD)

    #Given pivot USD, EUR->USD, missing USD->JPY
    def test_givenBank_WhenSetPivotCurrency_ThenPivotIsDefined(self):
        bank = Bank()

        bank.setPivotCurrency(Currency.USD)

        assert bank.pivot == Currency.USD
    #Given EUR->USD, USD->JPY, pivot USD
    def test_givenEURToJPYViaPivotUSD(self):
        bank = BankBuilder() \
            .with_rate(Currency.EUR, Currency.USD, 1.2) \
            .with_rate(Currency.USD, Currency.JPY, 100) \
            .build()

        bank.setPivotCurrency(Currency.USD)

        result = bank.convertMoney(Money.of(10, Currency.EUR), Currency.JPY)

        assert result == Money.of(1200, Currency.JPY)

    # Given EUR->USD, missing USD->JPY, pivot USD
    def test_givenMissingSecondRate_WhenConvertViaPivot_ThenThrows(self):
        # GIVEN
        bank = (
            BankBuilder()
            .with_rate(Currency.EUR, Currency.USD, 1.2)
            .build()
        )

        bank.setPivotCurrency(Currency.USD)

        # WHEN / THEN
        try:
            bank.convertMoney(Money.of(10, Currency.EUR), Currency.JPY)
            assert False
        except MissingExchangeRateError:
            assert True
    #Given pivot Money, which does not exist , then throws an exception
    def test_givenUnknownCurrency_WhenSetPivot_ThenThrows(self):
        # GIVEN
        bank = Bank()

        # WHEN / THEN
        try:
            bank.setPivotCurrency("XXX")
            assert False
        except ValueError:
            assert True

    def test_givenExistingPivot_WhenSetNewPivot_ThenThrows(self):
        # GIVEN
        bank = Bank()
        bank.setPivotCurrency(Currency.USD)

        # WHEN / THEN
        try:
            bank.setPivotCurrency(Currency.EUR)
            assert False
        except ValueError:
            assert True

    def test_givenRateAtoB_WhenConvertBtoA_ThenUseInverseRate(self):
        # GIVEN
        bank = (
            BankBuilder()
            .with_rate(Currency.EUR, Currency.USD, 2)
            .build()
        )

        # WHEN
        result = bank.convertMoney(Money.of(10, Currency.USD), Currency.EUR)

        # THEN
        assert result == Money.of(5, Currency.EUR)
