from django.shortcuts import render
from django.db.models import Sum
from .models import Cashout


def cashouts(request):
    # if superuser, renders table for cashouts of all users
    if request.user.is_superuser:
        cashouts = Cashout.objects.all()
        profitsum = Cashout.objects.all().aggregate(total=Sum('profit'))
        lpsum = Cashout.objects.all().aggregate(total=Sum('lp'))

    # if not superuser, renders user's tables
    else:
        cashouts = Cashout.objects.filter(client=request.user)
        profitsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('profit'))
        lpsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('lp'))
    
    # gets date of most recent cashout of any user
    last_updated = Cashout.objects.latest('date').date
    
    return render(
        request,
        'tables_app/cashouts.html', {
            'cashouts': cashouts,
            'profitsum': profitsum,
            'lpsum': lpsum,
            'last_updated': last_updated
        }
    )
