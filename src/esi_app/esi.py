from django.conf import settings
from esipy import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity


# Create the app
esi_app = EsiApp().get_latest_swagger


# Init the security object
esi_security = EsiSecurity(
    redirect_uri=settings.ESI_CALLBACK,
    client_id=settings.ESI_CLIENT_ID,
    secret_key=settings.ESI_SECRET_KEY,
    headers={'User-Agent': settings.ESI_USER_AGENT}
)


# Init the client
esi_client = EsiClient(
    retry_requests=True,
    headers={'User-Agent': settings.ESI_USER_AGENT},
    security=esi_security
)

