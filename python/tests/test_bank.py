import pytest

import re


from python.src.bank import Bank

from python.src.currency import Currency

from python.src.missing_exchange_rate_error import MissingExchangeRateError



class TestBank:

    def givenEuroAmount_WhenConvertToUsd_ThenReturnsUsdAmount(self):
        #GIVEN 
        from_currency= Currency.EUR
        to_currency = Currency.USD
        rate = 1.2
        bank = Bank.create(from_currency, to_currency, rate)
        amount = 10
        expected = 12
        # WHEN
        result = bank.convert(amount, from_currency, to_currency)
        # THEN
        assert result == expected

    def givenEuroAmount_WhenConvertToSameCurrency_ThenReturnsSameAmount(self):
        #GIVEN 
        from_currency= Currency.EUR
        to_currency = Currency.EUR
        rate = 1
        bank = Bank.create(from_currency, to_currency, rate)
        amount = 10
        expected = 10
        # WHEN
        result = bank.convert(amount, from_currency, to_currency)
        # THEN
        assert result == expected

    def givenEuroAmount_WhenConvertWithMissingExchangeRate_ThenThrowsException(self):
        #GIVEN
        from_currency= Currency.EUR
        to_currency = Currency.KRW
        bank = Bank()
        amount = 10
        # WHEN
        try:
            bank.convert(amount, from_currency, to_currency)
        # THEN
            assert False
        except MissingExchangeRateError:
            assert True


    def givenEuroAmount_WhenConvertWithDifferentExchangeRate_ThenReturnsDifferentFloats(self):

        #Given
        
        bank: Bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        assert bank.convert(10, Currency.EUR, Currency.USD) == 12


        bank.addExchangeRate(Currency.EUR, Currency.USD, 1.3)

        assert bank.convert(10, Currency.EUR, Currency.USD) == 13