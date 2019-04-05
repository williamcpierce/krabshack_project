from django.conf import settings
from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
import random
import hmac
import hashlib

# create the app
esi_app = EsiApp().get_latest_swagger

# init the security object
esi_security = EsiSecurity(
    redirect_uri=settings.ESI_CALLBACK,
    client_id=settings.ESI_CLIENT_ID,
    secret_key=settings.ESI_SECRET_KEY,
    headers={'User-Agent': settings.ESI_USER_AGENT}
)

# init the client
esi_client = EsiClient(
    retry_requests=True,
    headers={'User-Agent': settings.ESI_USER_AGENT},
    security=esi_security
)


def generate_token():
    # generates security token from secret key, saved in session
    chars = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    rand = random.SystemRandom()
    random_string = ''.join(rand.choice(chars) for _ in range(40))
    return hmac.new(
        settings.ESI_TOKEN_KEY.encode('utf-8'),
        random_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
