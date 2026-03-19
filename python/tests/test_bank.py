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
        """
        Quand un montant est converti dans la même devise,
        alors le même montant est retourné
        """

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


    def test_givenBank_WhenSetPivotCurrency_ThenPivotIsDefined(self):
        """
        Quand l'expert définit  le pivot, alors le pivot doit être une devise
        reconnu par la banque
        """
        bank = Bank()

        bank.setPivotCurrency(Currency.USD)

        assert bank.pivot == Currency.USD

    def test_givenEURToJPYViaPivotUSD(self):
        """
        Quand un montant est converti entre 2 devises non-pivot,
        alors la conversion passe par la devise pivot
        """
        bank = BankBuilder() \
            .with_rate(Currency.EUR, Currency.USD, 1.2) \
            .with_rate(Currency.USD, Currency.JPY, 100) \
            .build()

        bank.setPivotCurrency(Currency.USD)

        result = bank.convertMoney(Money.of(10, Currency.EUR), Currency.JPY)

        assert result == Money.of(1200, Currency.JPY)

    def test_givenMissingSecondRate_WhenConvertViaPivot_ThenThrows(self):
        """
        Quand un montant est convertie entre 2 devises non-pivot, alors la
        convertion passe par la devise pivot, mais si le taux de change entre
        la devise pivot et l'une des deux devises est manquant, alors une exception
        est levée
        """
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
        """
        Quand un expert définit une devise pivot qui n'est pas reconnu par
        la banque, alors une exception est levée
        """
        # GIVEN
        bank = Bank()

        # WHEN / THEN
        try:
            bank.setPivotCurrency("XXX")
            assert False
        except ValueError:
            assert True

    def test_givenExistingPivot_WhenSetNewPivot_ThenThrows(self):
        """
        Si une pivot currency est déjà définie et qu’on en définit une nouvelle
        , ERREUR
        """
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
        """
        Le taux inverse est égal à l’inverse du taux de change
        """
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

    def test_givenNegativeRate_WhenAddExchangeRate_ThenThrows(self):
        """Un taux de change ne peut etre négatif"""
        bank = Bank()

        try:
            bank.addExchangeRate(Currency.EUR, Currency.USD, -1)
            assert False
        except ValueError:
            assert True

    def test_givenExistingRate_WhenAddSameRate_ThenOverwrite(self):
        """Quand (un taux existe déjà pour cette devise) alors il est écrasé"""
        # GIVEN
        bank = (
            BankBuilder()
            .with_rate(Currency.EUR, Currency.USD, 1.08)
            .build()
        )

        # WHEN
        bank.addExchangeRate(Currency.EUR, Currency.USD, 1.10)

        # THEN
        result = bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD)
        assert result == Money.of(11, Currency.USD)

    def test_givenExistingRate_WhenAddExchangeRate_ThenOverwrite(self):
        """Quand un montant est multiplié, alors le multiplicateur
        doit être une valeur positive"""
        # GIVEN
        bank = (
            BankBuilder()
            .with_rate(Currency.EUR, Currency.USD, 1.08)
            .build()
        )

        # WHEN
        bank.addExchangeRate(Currency.EUR, Currency.USD, 1.10)

        # THEN
        result = bank.convertMoney(Money.of(10, Currency.EUR), Currency.USD)
        assert result == Money.of(11, Currency.USD)

    def test_givenNullPivot_WhenSetPivot_ThenThrows(self):
        """La pivot currency ne peut pas être null"""
        # GIVEN
        bank = Bank()

        # WHEN / THEN
        try:
            bank.setPivotCurrency(None)
            assert False
        except ValueError:
            assert True

    def test_givenNoPivot_WhenConvertBetweenTwoNonPivotCurrencies_ThenThrows(self):
        """
        Quand aucune pivot currency n’est définie,
        certaines conversions sont impossibles
        """
        # GIVEN
        bank = (
            BankBuilder()
            .with_rate(Currency.EUR, Currency.USD, 1.2)
            .with_rate(Currency.USD, Currency.JPY, 100)
            .build()
        )

        # WHEN / THEN
        try:
            bank.convertMoney(Money.of(10, Currency.EUR), Currency.JPY)
            assert False
        except MissingExchangeRateError:
            assert True
