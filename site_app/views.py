from django.shortcuts import render
from django.conf import settings
import requests


def couriers(request):
    return render(request, 'site_app/couriers.html')


def buyback(request):
    # get buyback rate
    with requests.Session() as s:
        download = s.get(settings.CSV_URL)
        decode = download.content.decode('utf-8')
        lprate = int(''.join(list(filter(str.isdigit, decode))))
    return render(
        request,
        'site_app/buyback.html',  {
            'lprate': lprate,
        }
    )


def home(request):
    return render(request, 'site_app/home.html')
