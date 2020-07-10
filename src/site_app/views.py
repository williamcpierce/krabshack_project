from django.conf import settings
from django.shortcuts import render

from .models import CourierRoute, LPRate, SiteContent


def couriers(request):
    # Get instructions and routes
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
    # Get instructions and lp rates
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
    # Get info
    info = SiteContent.objects.get(field_id='Home Info')

    return render(
        request,
        'site_app/home.html', {
            'info': info
        }
    )
