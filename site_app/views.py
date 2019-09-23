from django.shortcuts import render
from django.conf import settings
from .models import Rates
# import requests


def couriers(request):
    return render(request, 'site_app/couriers.html')


def buyback(request):
    # get buyback rate
    # with requests.Session() as s:
    #     download = s.get(settings.CSV_URL)
    #     decode = download.content.decode('utf-8')
    #     lprate = int(''.join(list(filter(str.isdigit, decode))))
    guristas_lprate = Rates.objects.get(lp_type="Guristas").lp_rate
    sanshas_lprate = Rates.objects.get(lp_type="Sanshas").lp_rate

    return render(
        request,
        'site_app/buyback.html',  {
            'guristas_lprate': guristas_lprate,
            'sanshas_lprate': sanshas_lprate
        }
    )


def home(request):
    return render(request, 'site_app/home.html')
