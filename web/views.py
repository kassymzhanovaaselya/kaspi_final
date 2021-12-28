import datetime
from decimal import Decimal
from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from database import DB
from configs import configs
import json
from account.account import Account
from templates import *


def index(request: HttpRequest) -> HttpResponse:
    customer = DB.pandas_row_to_customer(DB.get_object("customers", configs['current_customer_uuid']))
    print(customer)
    accounts = DB.get_objects_df('accounts')
    accounts = accounts[accounts['customer_id'] == str(customer.id_)]
    accounts['max'] = accounts.groupby('currency')["balance"].transform('max')
    accounts = json.loads(accounts.to_json(orient="records"))
    print(accounts)
    return render(request, 'index.html', context={"customer": customer, "accounts": accounts})


def create_account(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        new_acc = {
            "currency": request.POST['currency'],
            "balance": Decimal(0),
            "customer_id": configs['current_customer_uuid']}
        DB.save('accounts', new_acc)
        return index(request)

    if request.method == "GET":
        return render(request, 'create_account.html')
from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from database import DB
from configs import configs
import json
from account.account import Account
from templates import *


def index(request: HttpRequest) -> HttpResponse:
    customer = DB.pandas_row_to_customer(DB.get_object("customers", configs['current_customer_uuid']))
    print(customer)
    accounts = DB.get_objects_df('accounts')
    accounts = accounts[accounts['customer_id'] == str(customer.id_)]
    accounts['max'] = accounts.groupby('currency')["balance"].transform('max')
    accounts = json.loads(accounts.to_json(orient="records"))
    print(accounts)
    return render(request, 'index.html', context={"customer": customer, "accounts": accounts})


def create_account(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        new_acc = {
            "id": None,
            "currency": request.POST['currency'],
            "balance": Decimal(0),
            "customer_id": configs['current_customer_uuid']}
        DB.save('accounts', new_acc)
        return index(request)

    if request.method == "GET":
        return render(request, 'create_account.html')


def account_info(request: HttpRequest, id_) -> HttpResponse:
    account = DB.pandas_row_to_account(DB.get_object("accounts", UUID(id_)))
    print(account)
    # transactions = DB.get_objects_df('transactions')
    # transactions = transactions[(transactions['sender_id'] == id_) or transactions['recipient_id'] == id_]
    # transactions = json.loads(transactions.to_json(orient="records"))
    return render(request, 'account_info.html', context={'account': account})


def create_transaction(request: HttpRequest) -> HttpResponse:
    fromAcc = DB.pandas_row_to_account(DB.get_object('accounts', UUID(request.POST['from'])))
    toAcc = DB.pandas_row_to_account(DB.get_object('accounts', UUID(request.POST['to'])))

    new_tran = {
        "sender": fromAcc,
        "recipient": toAcc,
        "transfer_date": datetime.datetime.now(),
        "balance_brutto": Decimal(120),
        "balance_netto": None,
        "currency": fromAcc.currency,
        "status": "INPROCESS"
    }

