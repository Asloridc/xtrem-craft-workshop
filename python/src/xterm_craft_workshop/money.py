from .currency import Currency


class Money:
    def __init__(self, amount: float, currency: Currency):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    @staticmethod
    def of(amount: float, currency: Currency) -> "Money":
        if amount < 0:
            raise ValueError("un montant ne peut pas être négatif")
        return Money(amount, currency)

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("pas la meme currency")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, multiplier: float) -> "Money":
        return Money(self.amount * multiplier, self.currency)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division par zero")
            return Money(self.amount / other, self.currency)
        raise ValueError("type non supporté pour la division")
