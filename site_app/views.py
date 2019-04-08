from django.shortcuts import render


def couriers(request):
    return render(request, 'site_app/couriers.html')


def buyback(request):
    return render(request, 'site_app/buyback.html')


def home(request):
    return render(request, 'site_app/home.html')
