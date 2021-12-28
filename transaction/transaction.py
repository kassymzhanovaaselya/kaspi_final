import time
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from account.account import Account
from common.base_class import Base


class CurrencyMismatchError(ValueError):
    pass


class InsufficientFundsError(ValueError):
    pass


@dataclass
class Transaction(Base):
    sender: Account
    recipient: Account
    transfer_date: float
    balance_brutto: Decimal
    balance_netto: Decimal
    currency: str
    status: str

    def transfer(self) -> str:
        assert isinstance(self.sender, Account)
        assert isinstance(self.recipient, Account)

        before_transfer = self.recipient.balance - self.sender.balance

        if self.sender.currency != self.recipient.currency:
            raise CurrencyMismatchError
        elif self.sender.balance < self.balance_brutto:
            raise InsufficientFundsError
        else:
            self.sender.balance -= self.balance_brutto
            self.recipient.balance += self.balance_brutto
            after_transfer = self.recipient.balance - self.sender.balance
            assert before_transfer == (after_transfer - Decimal(2)*self.balance_brutto)

        return "success"
