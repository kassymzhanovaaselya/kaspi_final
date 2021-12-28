from database.database import Database
from account.account import Account


class TestDatabase:
    def test_connection(self, connection_string: str) -> None:
        database = Database(connection=connection_string)
        test_acc = Account.random()
        # test INSERT
        database.save("accounts", test_acc.to_json())
        all_accounts = database.get_objects(table_name="accounts")
        print(all_accounts)

        # test UPDATE
        another_acc = Account.random()
        another_acc.id_ = test_acc.id_
        database.save("accounts", test_acc.to_json())
        all_accounts = database.get_objects(table_name="accounts")
        print(all_accounts)
        database.close_connection()
