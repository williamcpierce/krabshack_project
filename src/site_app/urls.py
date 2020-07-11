from django.urls import path

from .views import buyback, couriers


urlpatterns = [
    path('services/buyback/', buyback, name='buyback'),
    path('services/couriers/', couriers, name='couriers')
]
