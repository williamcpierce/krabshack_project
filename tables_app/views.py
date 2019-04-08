from django.shortcuts import render
from django.db.models import Sum
from .models import Cashout


def cashouts(request):
    # renders table for cashouts of all users, if superuser
    if request.user.is_superuser:
        table = Cashout.objects.all()
        profitsum = Cashout.objects.all().aggregate(total=Sum('profit'))
        lpsum = Cashout.objects.all().aggregate(total=Sum('lp'))
        return render(
            request,
            'tables_app/cashouts.html', {
                'table': table,
                'profitsum': profitsum,
                'lpsum': lpsum
            }
        )
    # if not superuser, renders user's tables
    else:
        table = Cashout.objects.filter(client=request.user)
        profitsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('profit'))
        lpsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('lp'))
        return render(
            request,
            'tables_app/cashouts.html', {
                'table': table,
                'profitsum': profitsum,
                'lpsum': lpsum
            }
        )
