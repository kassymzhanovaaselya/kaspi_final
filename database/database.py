import json
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4
import psycopg2
import pandas as pd
from pandas import DataFrame, Series
from account.account import Account
from customer.customer import Customer
from configs import configs
from transaction.transaction import Transaction


class ObjectNotFound(ValueError):
    pass


class FieldsMismatchError(ValueError):
    pass


class Database:
    def __init__(self, connection: str,  *args, **kwargs):
        self.conn = psycopg2.connect(connection)
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id varchar primary key
                , currency varchar
                , balance decimal
                , customer_id varchar
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS commissions (
                id varchar primary key
                , type_code varchar
                , percentage numeric(18, 2)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id varchar primary key
                , first_name varchar
                , last_name varchar
                , age decimal
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id varchar primary key
                , sender_id varchar
                , recipient_id varchar 
                , transfer_date timestamp 
                , balance_brutto float
                , balance_netto float 
                , currency varchar 
                , status varchar 
            );
        """)

        """
            FOR WEB APPLICATION LET'S SAVE STATIC CUSTOMER WHICH CAN HAVE SEVERAL ACCOUNTS
        """
        if len(self.get_objects('customers')) == 0:
            uuid_str = configs['current_customer_uuid']
            current_customer = Customer(UUID(uuid_str),
                                        "Assel",
                                        "Kassymzhanova",
                                        Decimal(20))
            self.save('customers', current_customer.to_json())

            first_account = Account(uuid4(),
                                    "USD",
                                    Decimal(100),
                                    UUID(uuid_str))
            self.save("accounts", first_account.to_json())

        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def set_fields_mapper(self, obj):
        mapped = ""
        for key, value in obj.items():
            if key != 'id':
                mapped += f" {key} = %s,"
        return mapped[:-1]

    def save(self, table_name, obj) -> None:
        if obj['id'] is None:
            obj['id'] = uuid4()
        obj['id'] = str(obj['id'])

        print(f"OBJECT ::::: {obj}")
        mapper = self.set_fields_mapper(obj)

        values_tuple = tuple([value for key, value in obj.items() if key != "id"])
        query = "UPDATE {0} SET {1} WHERE id = '{2}';".format(table_name, mapper, obj['id'])
        print(f"QUERY :::: {query}")
        cur = self.conn.cursor()
        cur.execute(query, values_tuple)
        rows_count = cur.rowcount
        self.conn.commit()
        print("-----------------UPDATED-----------------")

        print("ROWS COUNT", rows_count)
        if rows_count == 0:
            fields_text = ', '.join(obj.keys())
            objects = tuple(obj.values())
            print(f"FIELDS TEXT ::: {fields_text}")
            print(f"OBJECTSSSS :::: {objects}")
            query = "insert into {0} ({1}) values %s".format(table_name, fields_text)
            cur = self.conn.cursor()
            cur.execute(query, (objects, ))
            self.conn.commit()
            print("-----------------INSERTED-----------------")

    def clear_all(self, table_name) -> None:
        cur = self.conn.cursor()
        cur.execute(f"delete from {table_name};")
        self.conn.commit()

    def get_objects_df(self, table_name) -> DataFrame:
        cur = self.conn.cursor()
        cur.execute(f"select * from {table_name};")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        # return [self.pandas_row_to_account(row) for index, row in df.iterrows()]
        return df

    def get_objects(self, table_name):
        df = self.get_objects_df(table_name)
        if table_name == "accounts":
            return [self.pandas_row_to_account(row) for index, row in df.iterrows()]
        elif table_name == "customers":
            return [self.pandas_row_to_customer(row) for index, row in df.iterrows()]
        elif table_name == "transactions":
            return [self.pandas_row_to_transaction(row) for index, row in df.iterrows()]

    def pandas_row_to_account(self, row: Series) -> Account:
        return Account(
            id_=UUID(row["id"]),
            currency=row["currency"],
            balance=row["balance"],
            customer_id=UUID(row['customer_id'])
        )

    def pandas_row_to_customer(self, row: Series) -> Customer:
        return Customer(
            id_=UUID(row["id"]),
            first_name=row["first_name"],
            last_name=row["last_name"],
            age=Decimal(row['age']),
        )

    def pandas_row_to_transaction(self, row: Series) -> Transaction:
        sender = self.pandas_row_to_account(self.get_object("accounts", UUID(row['sender_id'])))
        recipient = self.pandas_row_to_account(self.get_object("accounts", UUID(row['recipient_id'])))
        return Transaction(
            sender=UUID(row["sender_id"]),
            recipient=UUID(row["recipient_id"]),
            transfer_date=float(row["transfer_date"]),
            balance_brutto=Decimal(row["balance_brutto"]),
            balance_netto=Decimal(row["balance_netto"]),
            currency=row["currency"],
            status=row["status"]
        )

    def get_object(self, table_name, id_: UUID) -> Series:
        cur = self.conn.cursor()
        cur.execute(f"select * from {table_name} where id = %s;", (str(id_),))
        print("Trying to find", str(id_))
        data = cur.fetchall()
        if len(data) == 0:
            raise ObjectNotFound("Postgres: Object not found")
        cols = [x[0] for x in cur.description]

        df = pd.DataFrame(data, columns=cols)
        # return self.pandas_row_to_account(row=df.iloc[0])
        return df.iloc[0]

    def delete(self, table_name: str, id_: UUID) -> bool:
        cur = self.conn.cursor()
        print(f"Trying to delete from {table_name} with  ", str(id_))
        cur.execute(f"delete from {table_name} where id = %s;", (str(id_),))
        self.conn.commit()
        if cur.rowcount == 0:
            return False
        return True
