from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from database import DB
from configs import configs
from templates import *


def index(request: HttpRequest) -> HttpResponse:
    customer = DB.get_object("customers", configs['current_customer_uuid'])
    accounts = DB.get_objects('accounts')
    # customer_accounts = accounts[accounts['customer_id'] == customer.id_]
    return render(request, 'index.html', context={"customer": customer})