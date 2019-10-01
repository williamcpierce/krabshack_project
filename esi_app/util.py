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
