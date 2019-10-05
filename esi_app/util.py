from django.conf import settings
import random
import hmac
import hashlib


def generate_token():
    """
    generates security token from secret key, saved in session
    """
    character_set = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    random_value = random.SystemRandom()
    random_string = ''.join(random_value.choice(character_set) for _ in range(40))
    return hmac.new(
        settings.ESI_TOKEN_KEY.encode('utf-8'),
        random_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def parse_lp(lp_values, corp_id):
    """
    parses character lp esi response to return corp lp values
    """
    corp_lp = 0
    for item in lp_values:
        if item.get('corporation_id') == corp_id:
            corp_lp = item.get('loyalty_points')
            break
    return corp_lp


def parse_market_orders(market_orders):
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
        "sell_order_min": sell_order_min, 
        "buy_order_max": buy_order_max
    }


def parse_market_history(market_history):
    monthly_volume = 0
    days = 0
    for item in market_history[::-1]:
        monthly_volume += item.get('volume')
        days += 1
        if days == 30:
            break
    daily_volume = monthly_volume / days
    return daily_volume
