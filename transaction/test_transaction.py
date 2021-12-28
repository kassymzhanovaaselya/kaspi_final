
import time
from decimal import Decimal

import pytest
from uuid import uuid4
from transaction.transaction import Transaction
from account.account import Account


class TestTransaction:
    def test_customer_create(self) -> Transaction:
        tran_id = uuid4()
        sender_acc = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(10),
            customer_id=uuid4()
        )
        recipient_acc = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(17),
            customer_id=uuid4()
        )

        assert isinstance(sender_acc, Account)
        assert isinstance(recipient_acc, Account)

        current_time = time.time()

        transaction = Transaction(
            id_=tran_id,
            sender=sender_acc,
            recipient=recipient_acc,
            transfer_date=current_time,
            balance_brutto=Decimal(3),
            balance_netto=Decimal(3),
            currency="KZT",
            status="success"
        )

        assert isinstance(transaction, Transaction)
        assert isinstance(transaction.balance_brutto, Decimal)
        assert transaction.currency == "KZT"

        return transaction

    def test_transfer(self) -> None:
        transaction = self.test_customer_create()
        assert isinstance(transaction, Transaction)

        transfer_result = transaction.transfer()
        assert transfer_result == "success"
