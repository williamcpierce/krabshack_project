from django.urls import path

from .views import buyback, couriers, home


urlpatterns = [
    path('', home, name='home'),
    path('services/buyback/', buyback, name='buyback'),
    path('services/couriers/', couriers, name='couriers')
]
