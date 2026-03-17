from src.bank import Bank
from src.currency import Currency
from src.portfolio import Portfolio
from src.money import Money


class TestPortfolio:
    def test_should_return_500_when_adding_500_to_empty_portfolio(self):
        # Given an empty portfolio
        portfolio = Portfolio()
        # And a bank who accepts it
        bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        # When I add 500 to the portfolio
        portfolio.add(500, Currency.USD)

        # Then I should see 500
        assert portfolio.evaluate(bank, Currency.USD).amount == 500

    def test_should_add_10_usd_to_existing_portfolio(self):
        # Given a portfolio containing some amount
        portfolio = Portfolio()
        portfolio.add(500, Currency.USD)
        # And a bank who accepts it
        bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        # When I add 10 USD to the portfolio
        portfolio.add(10, Currency.USD)

        # Then I should see +10 USD (total = 510)
        assert portfolio.evaluate(bank, Currency.USD).amount == 510

    def test_should_return_2000_jpy_when_portfolio_contains_10_usd_and_500_jpy(self):
        # Given un portfolio contenant 10 USD
        portfolio = Portfolio()
        portfolio.add(10, Currency.USD)
        # And contenant 500 JPY
        portfolio.add(500, Currency.JPY)
        # And une banque avec un taux de change USD vers JPY de 150
        bank = Bank.create(Currency.USD, Currency.JPY, 150)

        # When j'évalue le portfolio vers la devise JPY
        result = portfolio.evaluate(bank, Currency.JPY)

        # Then je devrais recevoir 2000 JPY
        assert result.amount == 2000

    def test_should_return_2_08_usd_when_portfolio_contains_1_usd_and_1_eur(self):
        # Given un portfolio contenant 1 USD
        portfolio = Portfolio()
        portfolio.add(1, Currency.USD)
        # And contenant 1 EUR
        portfolio.add(1, Currency.EUR)
        # And une banque avec un taux de change EUR vers USD de 1.08
        bank = Bank.create(Currency.EUR, Currency.USD, 1.08)

        # When j'évalue le portfolio vers la devise USD
        result = portfolio.evaluate(bank, Currency.USD)

        # Then je devrais recevoir 2.08 USD
        assert result.amount == 2.08

    def test_should_return_0_when_evaluating_empty_portfolio(self):
        # Given a portfolio empty
        portfolio = Portfolio()
        # And a bank who accepts it
        bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        # When I evaluate the portfolio
        result = portfolio.evaluate(bank, Currency.USD)

        # Then I should see 0
        assert result.amount == 0