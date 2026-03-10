# Test Driven Development

Notre mission pour cette itération est d'implémenter la notion de portefeuille à partir des exemples obtenus pendant la session d'[example mapping](./06-example-mapping.md).

## Écrire un premier test en utilisant un premier exemple :
- Écrire votre code en pratiquant le `Test Driven Development` : écrire un test rouge, faire passer le test, refactorer.
```Python
 def test_should_return_500_when_adding_500_to_empty_portfolio(self):
        # Given an empty portfolio
        portfolio = Portfolio()
        # And a bank who accepts it
        bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        # When I add 500 to the portfolio
        portfolio.add(500, Currency.USD)

        # Then I should see 500
        assert portfolio.evaluate(bank, Currency.USD) == 500

def test_should_add_10_usd_to_existing_portfolio(self):
        # Given a portfolio containing some amount
        portfolio = Portfolio()
        portfolio.add(500, Currency.USD)
        # And a bank who accepts it
        bank = Bank.create(Currency.EUR, Currency.USD, 1.2)

        # When I add 10 USD to the portfolio
        portfolio.add(10, Currency.USD)

        # Then I should see +10 USD (total = 510)
        assert portfolio.evaluate(bank, Currency.USD) == 510
``` 
- Prendre un peu de temps pour découvrir comment [générer votre code par l'usage](https://xtrem-tdd.netlify.app/Flavours/generate-code-from-usage).

Itérez sur les différents exemples jusqu'à ce que la User Story soit terminée.

## Rétrospective

**3 faits et une question à propos du Test Driven Development**

Individuellement, donnez les 3 idées les plus importantes sur le TDD et une question qui reste en suspend.
On commence par écire une partie des tests puis on utiise la méthode quick and dirty et ensuite on refactor.

Red -> Green -> Refactor : On écrit d'abord un test qui échoue (RED), puis on écrit le code minimal pour le faire passer (GREEN), et enfin on améliore le code sans changer le fonctionnement (REFACTOR).

On écrite le test AVANT d'écrire le code.

Avancer par petits pas : Chaque cycle TDD est un petit incrément. On écrit des tests minimaux,


Comment gère-t-on les cas plus complexes comme la conversion multi-devises (ex. ajouter des EUR et des KRW dans le portfolio et évaluer en USD) ? Faut-il un test par combinaison de devises ?
> Qu'avez-vous appris de l'introduction de nouveaux rôles en mob programming ?
