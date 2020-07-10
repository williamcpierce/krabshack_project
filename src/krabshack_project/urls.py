from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from data_app import views as data_views
from esi_app import views as esi_views
from site_app import views as site_views


urlpatterns = [
    url(r'^$', site_views.home, name='home'),
    url(r'^services/couriers/$', site_views.couriers, name='couriers'),
    url(r'^services/buyback/$', site_views.buyback, name='buyback'),
    url(r'^data/cashouts/$', data_views.cashouts, name='cashouts'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^esi/callback/', esi_views.callback, name='callback'),
    url(r'^esi/login/', esi_views.login, name='login'),
    url(r'^esi/lp/', esi_views.esilp, name='esilp'),
    url(r'^esi/market/update', esi_views.esimarketupdate, name='esimarketupdate'),
    url(r'^esi/market/', esi_views.esimarket, name='esimarket'),
    url(r'^esi/moon/', esi_views.esimoon, name='esimmoon'),
]
