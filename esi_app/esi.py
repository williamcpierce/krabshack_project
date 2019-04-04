from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity
from esi_app import config
import random
import hmac
import hashlib

# create the app
esi_app = EsiApp().get_latest_swagger

# init the security object
esi_security = EsiSecurity(
    redirect_uri=config.ESI_CALLBACK,
    client_id=config.ESI_CLIENT_ID,
    secret_key=config.ESI_SECRET_KEY,
    headers={'User-Agent': config.ESI_USER_AGENT}
)

# init the client
esi_client = EsiClient(
    retry_requests=True,
    headers={'User-Agent': config.ESI_USER_AGENT},
    security=esi_security
)


def generate_token():
    # generates security token from secret key, saved in session
    chars = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    rand = random.SystemRandom()
    random_string = ''.join(rand.choice(chars) for _ in range(40))
    return hmac.new(
        config.SECRET_KEY.encode('utf-8'),
        random_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
