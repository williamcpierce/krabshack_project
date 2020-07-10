from django.db.models import Sum
from django.shortcuts import render

from .models import Cashout


def cashouts(request):
    """Display user cashout data."""

    # Initialize variables
    totals = {}

    # If superuser, renders table for cashouts of all users
    if request.user.is_superuser:
        cashouts = Cashout.objects.all()
        totals['profitsum'] = Cashout.objects.all().aggregate(total=Sum('profit'))
        totals['lpsum'] = Cashout.objects.all().aggregate(total=Sum('lp'))

    # If not superuser, renders user's tables
    else:
        cashouts = Cashout.objects.filter(client=request.user)
        totals['profitsum'] = Cashout.objects.filter(client=request.user).aggregate(total=Sum('profit'))
        totals['lpsum'] = Cashout.objects.filter(client=request.user).aggregate(total=Sum('lp'))

    # Gets date of most recent cashout of any user
    last_updated = Cashout.objects.latest('date').date

    return render(
        request,
        'data_app/cashouts.html', {
            'cashouts': cashouts,
            'totals': totals,
            'last_updated': last_updated,
            'subheader': 'Cashout Data'
        }
    )
