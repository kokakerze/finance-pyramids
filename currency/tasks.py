from datetime import date
from decimal import Decimal

import requests
from celery import shared_task
from requests.exceptions import HTTPError


# from django.conf import settings


def database_filler(buy, ccy, sale, source):
    from currency.models import Currency
    cr_last = Currency.objects.filter(currency=ccy, source=source).last()
    if cr_last is None or (cr_last.buy != Decimal(buy) or cr_last.sale != Decimal(sale)):
        Currency.objects.create(currency=ccy, source=source, buy=Decimal(buy), sale=Decimal(sale))


@shared_task
def debug():
    print("------------------------------>Iamhere")


@shared_task
def parse_private_bank():
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    response = requests.get(url)

    try:
        response = requests.get(url)
        # error if response_status_code will be not 200
        response.raise_for_status()
    except HTTPError as http_err:
        # TODO: log http_error
        pass
    except Exception as err:
        # TODO: log error
        pass

    currency_map = {"USD": 1, "EUR": 2, }

    data = response.json()
    source = 1
    for row in data:
        if row["ccy"] in currency_map:
            buy = row["buy"]
            sale = row["sale"]
            ccy = currency_map[row["ccy"]]

            database_filler(buy, ccy, sale, source)


@shared_task
def parse_mono_bank():
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)

    try:
        response = requests.get(url)
        # error if response_status_code will be not 200
        response.raise_for_status()
    except HTTPError as http_err:
        # TODO: log http_error
        pass
    except Exception as err:
        # TODO: log error
        pass

    currency_map = {840: 1, 978: 2, }

    data = response.json()
    source = 2
    for row in data:
        if row["currencyCodeA"] in currency_map and row["currencyCodeB"] == 980:
            buy = round(Decimal(row["rateBuy"]), 2)
            sale = round(Decimal(row["rateSell"]), 2)
            ccy = str(currency_map[row["currencyCodeA"]])
            database_filler(buy, ccy, sale, source)


@shared_task
def parse_yahoo():
    from datetime import timedelta

    from yahoofinancials import YahooFinancials
    currencies = ['EURUAH=X', 'USDUAH=X']
    source = 3
    currency_map = {'USDUAH=X': 1, 'EURUAH=X': 2}
    for cur in currencies:
        yahoo_financials_currencies = YahooFinancials(cur)
        yesterday = date.today() - timedelta(days=1)
        buy = round(Decimal(yahoo_financials_currencies.get_historical_price_data(str(yesterday), str(yesterday), "daily")[cur][
            'prices'][0]['close']),2)
        sale = round(Decimal(yahoo_financials_currencies.get_historical_price_data(str(yesterday), str(yesterday), "daily")[cur][
            'prices'][0]['close']),2)
        ccy = currency_map[cur]
        database_filler(buy, ccy, sale, source)


@shared_task
def parse_vkurse_dp():
    url = "http://vkurse.dp.ua/course.json"
    response = requests.get(url)

    try:
        response = requests.get(url)
        # error if response_status_code will be not 200
        response.raise_for_status()
    except HTTPError as http_err:
        # TODO: log http_error
        pass
    except Exception as err:
        # TODO: log error
        pass

    currency_map = {"Dollar": 1, "Euro": 2, }

    data = response.json()
    source = 4
    for row in data:
        if row in currency_map:
            buy = data[row]["buy"]
            sale = data[row]["sale"]
            ccy = str(currency_map[row])
            database_filler(buy, ccy, sale, source)
