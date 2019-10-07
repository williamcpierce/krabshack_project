from django.shortcuts import render
from django.conf import settings
from .models import LPRate, SiteContent, CourierRoute


def couriers(request):
    # get instructions and routes
    instructions = SiteContent.objects.get(field_id='Courier Instructions')
    routes = CourierRoute.objects.all()
    last_updated = CourierRoute.objects.latest('last_updated').last_updated
    
    return render(
        request,
        'site_app/couriers.html', {
            'instructions': instructions,
            'routes': routes,
            'last_updated': last_updated
        }
    )


def buyback(request):
    # get instructions and lp rates
    instructions = SiteContent.objects.get(field_id='Buyback Instructions')
    guristas_lp_rate = LPRate.objects.get(lp_type='Guristas').lp_rate
    sanshas_lp_rate = LPRate.objects.get(lp_type='Sanshas').lp_rate
    ded_lp_rate = LPRate.objects.get(lp_type='DED').lp_rate

    return render(
        request,
        'site_app/buyback.html', {
            'guristas_lp_rate': guristas_lp_rate,
            'sanshas_lp_rate': sanshas_lp_rate,
            'ded_lp_rate': ded_lp_rate,
            'instructions': instructions
        }
    )


def home(request):
    # get info
    info = SiteContent.objects.get(field_id='Home Info')

    return render(
        request,
        'site_app/home.html', {
            'info': info
        }
    )
