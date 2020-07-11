from django.urls import path

from .views import cashouts


urlpatterns = [
    path('cashouts/', cashouts, name='cashouts')
]
