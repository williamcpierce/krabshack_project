from django.urls import path

from .views import FitFix


urlpatterns = [
    path('', FitFix.as_view(), name='FitFix'),
]
