from django.conf import settings
from operator import itemgetter
import random
import hmac
import hashlib
import requests


def generate_token():
    """Generates security token from secret key, saved in session."""

    character_set = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    random_value = random.SystemRandom()
    random_string = ''.join(random_value.choice(character_set) for _ in range(40))

    digest = hmac.new(
        settings.ESI_TOKEN_KEY.encode('utf-8'),
        random_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return digest


def parse_lp(lp_values, corp_id):
    """Parses character lp esi response to return corp lp values."""

    corp_lp = 0
    for item in lp_values:
        if item.get('corporation_id') == corp_id:
            corp_lp = item.get('loyalty_points')
            break

    return corp_lp


def parse_market_orders(market_orders):
    """Parses market orders to return minimum sell and maximum buy orders in Jita 4-4."""

    sell_order_min = 10000000000
    buy_order_max = 0

    for item in market_orders:
        if item.get('system_id') == 30000142:
            if item.get('is_buy_order') is False:
                if item.get('price') < sell_order_min:
                    sell_order_min = item.get('price')
            else:
                if item.get('price') > buy_order_max:
                    buy_order_max = item.get('price')

    return {
        'sell_order_min': sell_order_min,
        'buy_order_max': buy_order_max
    }


def parse_market_history(market_history):
    """Parses market history to average daily volume over the last week."""

    period_volume = 0
    start_day = 2
    end_day = 8
    day = 1

    for item in market_history:
        if day >= start_day and day <= end_day:
            period_volume += item.get('volume')
        if day > end_day:
            break
        day += 1

    daily_volume = round(
        period_volume / (end_day - start_day + 1),
        2
    )

    return daily_volume


def build_esi_url(**kwargs):
    """Constructs a url for public esi data requests, either market orders or history."""

    if kwargs.get('op') == 'orders':
        response = (
            'https://esi.evetech.net/latest/markets/' +
            str(kwargs.get('region_id')) +
            '/orders/?' +
            'order_type=' +
            kwargs.get('order_type') +
            '&type_id=' +
            str(kwargs.get('type_id'))
        )

    if kwargs.get('op') == 'history':
        response = (
            'https://esi.evetech.net/latest/markets/' +
            str(kwargs.get('region_id')) +
            '/history/?' +
            'type_id=' +
            str(kwargs.get('type_id'))
        )

    if kwargs.get('op') == 'public':
        response = (
            'https://esi.evetech.net/latest/characters/' +
            str(kwargs.get('character_id'))
        )

    return response


def esi_request(*args, **kwargs):
    """Wraps build_esi_url and makes the actual http request."""

    return requests.get(build_esi_url(*args, **kwargs))


def get_corp(character_id):
    """Returns corpation id given character id."""

    esi_response = esi_request(
        op='public',
        character_id=character_id
    )

    corporation_id = esi_response.json().get('corporation_id')

    return corporation_id


def append_list(list1, list2):
    """Appends two lists, removing duplicates."""

    result = []
    list1.extend(list2)

    for item in list1:
        if item not in result:
            result.append(item)

    return result


def sort_list(result):
    """Sorts list by date descending."""

    result.sort(key=itemgetter('date'), reverse=True)

    return result
