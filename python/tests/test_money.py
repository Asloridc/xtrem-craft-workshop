import pytest

from src.currency import Currency

# from src.money_calculator import MoneyCalculator
from src.money import Money


class TestMoney:
    def test_add_in_usd_returns_value(self):
        five_usd = Money.of(5, Currency.USD)
        ten_usd = Money.of(10, Currency.USD)
        result = five_usd + ten_usd
        assert result == Money.of(15, Currency.USD)

    def test_multiply_in_euros_returns_positive_number(self):
        five_euros = Money.of(5, Currency.EUR)
        result = five_euros * 2
        assert result == Money.of(10, Currency.EUR)

    def test_divide_in_korean_won_returns_float(self):
        ten_thousand_won = Money.of(10000, Currency.KRW)
        result = ten_thousand_won / 4
        assert result == Money.of(2500, Currency.KRW)

    def test_add_different_currencies(self):
        five_usd = Money.of(5, Currency.USD)
        ten_euros = Money.of(10, Currency.EUR)

        with pytest.raises(ValueError):
            _ = five_usd + ten_euros

    def test_divide_by_0(self):
        five_usd = Money.of(5, Currency.USD)

        with pytest.raises(ZeroDivisionError):
            _ = five_usd / 0

    def test_negative_amount(self):
        with pytest.raises(ValueError):
            _ = Money.of(-5, Currency.USD)
