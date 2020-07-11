from django.urls import path

from .views import callback, esilp, esimarket, esimarketupdate, esimoon, login


urlpatterns = [
    path('callback/', callback, name='callback'),
    path('login/', login, name='login'),
    path('lp/', esilp, name='esilp'),
    path('market/update/', esimarketupdate, name='esimarketupdate'),
    path('market/', esimarket, name='esimarket'),
    path('moon/', esimoon, name='esimoon')
]
