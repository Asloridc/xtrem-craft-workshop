from typing import Dict
from .currency import Currency
from .missing_exchange_rate_error import MissingExchangeRateError
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class Bank:
    _exchange_rate: Dict[str, float] = {}

    def __init__(self, exchange_rate = {}) -> None:
        args = [exchange_rate]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBankǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBankǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBankǁ__init____mutmut_orig(self, exchange_rate = {}) -> None:
        self._exchange_rate = exchange_rate

    def xǁBankǁ__init____mutmut_1(self, exchange_rate = {}) -> None:
        self._exchange_rate = None
    
    xǁBankǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBankǁ__init____mutmut_1': xǁBankǁ__init____mutmut_1
    }
    xǁBankǁ__init____mutmut_orig.__name__ = 'xǁBankǁ__init__'

    @staticmethod
    def create(currency1: Currency, currency2: Currency, rate: float) -> "Bank":
        bank = Bank({})
        bank.addExchangeRate(currency1, currency2, rate)

        return bank
    
    def addExchangeRate(self, from_currency: Currency, to_currency: Currency, rate: float) -> None:
        args = [from_currency, to_currency, rate]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBankǁaddExchangeRate__mutmut_orig'), object.__getattribute__(self, 'xǁBankǁaddExchangeRate__mutmut_mutants'), args, kwargs, self)
    
    def xǁBankǁaddExchangeRate__mutmut_orig(self, from_currency: Currency, to_currency: Currency, rate: float) -> None:
        self._exchange_rate[f'{from_currency.value}+->{to_currency.value}'] = rate
    
    def xǁBankǁaddExchangeRate__mutmut_1(self, from_currency: Currency, to_currency: Currency, rate: float) -> None:
        self._exchange_rate[f'{from_currency.value}+->{to_currency.value}'] = None
    
    xǁBankǁaddExchangeRate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBankǁaddExchangeRate__mutmut_1': xǁBankǁaddExchangeRate__mutmut_1
    }
    xǁBankǁaddExchangeRate__mutmut_orig.__name__ = 'xǁBankǁaddExchangeRate'

    def convert(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        args = [amount, from_currency, to_currency]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBankǁconvert__mutmut_orig'), object.__getattribute__(self, 'xǁBankǁconvert__mutmut_mutants'), args, kwargs, self)

    def xǁBankǁconvert__mutmut_orig(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_1(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_2(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(None, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_3(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, None):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_4(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_5(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, ):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_6(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(None, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_7(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, None)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_8(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_9(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, )):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_10(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount / self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, to_currency)

    def xǁBankǁconvert__mutmut_11(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(None, to_currency)

    def xǁBankǁconvert__mutmut_12(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, None)

    def xǁBankǁconvert__mutmut_13(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(to_currency)

    def xǁBankǁconvert__mutmut_14(self, amount: float, from_currency: Currency, to_currency: Currency) -> float:
        if not self.needExchangeRate(from_currency, to_currency):
            return amount
        if (self.hasExchangeRate(from_currency, to_currency)):
            return amount * self._exchange_rate[f'{from_currency.value}->{to_currency.value}']
        raise MissingExchangeRateError(from_currency, )
    
    xǁBankǁconvert__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBankǁconvert__mutmut_1': xǁBankǁconvert__mutmut_1, 
        'xǁBankǁconvert__mutmut_2': xǁBankǁconvert__mutmut_2, 
        'xǁBankǁconvert__mutmut_3': xǁBankǁconvert__mutmut_3, 
        'xǁBankǁconvert__mutmut_4': xǁBankǁconvert__mutmut_4, 
        'xǁBankǁconvert__mutmut_5': xǁBankǁconvert__mutmut_5, 
        'xǁBankǁconvert__mutmut_6': xǁBankǁconvert__mutmut_6, 
        'xǁBankǁconvert__mutmut_7': xǁBankǁconvert__mutmut_7, 
        'xǁBankǁconvert__mutmut_8': xǁBankǁconvert__mutmut_8, 
        'xǁBankǁconvert__mutmut_9': xǁBankǁconvert__mutmut_9, 
        'xǁBankǁconvert__mutmut_10': xǁBankǁconvert__mutmut_10, 
        'xǁBankǁconvert__mutmut_11': xǁBankǁconvert__mutmut_11, 
        'xǁBankǁconvert__mutmut_12': xǁBankǁconvert__mutmut_12, 
        'xǁBankǁconvert__mutmut_13': xǁBankǁconvert__mutmut_13, 
        'xǁBankǁconvert__mutmut_14': xǁBankǁconvert__mutmut_14
    }
    xǁBankǁconvert__mutmut_orig.__name__ = 'xǁBankǁconvert'
    
    def needExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        args = [from_currency, to_currency]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBankǁneedExchangeRate__mutmut_orig'), object.__getattribute__(self, 'xǁBankǁneedExchangeRate__mutmut_mutants'), args, kwargs, self)
    
    def xǁBankǁneedExchangeRate__mutmut_orig(self, from_currency: Currency, to_currency: Currency) -> bool:
        return from_currency.value != to_currency.value
    
    def xǁBankǁneedExchangeRate__mutmut_1(self, from_currency: Currency, to_currency: Currency) -> bool:
        return from_currency.value == to_currency.value
    
    xǁBankǁneedExchangeRate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBankǁneedExchangeRate__mutmut_1': xǁBankǁneedExchangeRate__mutmut_1
    }
    xǁBankǁneedExchangeRate__mutmut_orig.__name__ = 'xǁBankǁneedExchangeRate'

    def hasExchangeRate(self, from_currency: Currency, to_currency: Currency) -> bool:
        args = [from_currency, to_currency]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBankǁhasExchangeRate__mutmut_orig'), object.__getattribute__(self, 'xǁBankǁhasExchangeRate__mutmut_mutants'), args, kwargs, self)

    def xǁBankǁhasExchangeRate__mutmut_orig(self, from_currency: Currency, to_currency: Currency) -> bool:
        return f'{from_currency.value}->{to_currency.value}' in self._exchange_rate

    def xǁBankǁhasExchangeRate__mutmut_1(self, from_currency: Currency, to_currency: Currency) -> bool:
        return f'{from_currency.value}->{to_currency.value}' not in self._exchange_rate
    
    xǁBankǁhasExchangeRate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBankǁhasExchangeRate__mutmut_1': xǁBankǁhasExchangeRate__mutmut_1
    }
    xǁBankǁhasExchangeRate__mutmut_orig.__name__ = 'xǁBankǁhasExchangeRate'