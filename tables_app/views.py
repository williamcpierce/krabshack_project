from django.shortcuts import render
from django.db.models import Sum
from .models import Cashout


def cashouts(request):
    if request.user.is_superuser:
        uid = request.user.social_auth.get(provider='eveonline').uid
        table = Cashout.objects.all()
        profitsum = Cashout.objects.all().aggregate(total=Sum('profit'))
        lpsum = Cashout.objects.all().aggregate(total=Sum('lp'))
        return render(
            request,
            'tables_app/cashouts.html', {
                'table': table,
                'profitsum': profitsum,
                'lpsum': lpsum,
                'uid': uid
            }
        )
    else:
        if request.user.is_authenticated:
            uid = request.user.social_auth.get(provider='eveonline').uid
            table = Cashout.objects.filter(client=request.user)
            profitsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('profit'))
            lpsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('lp'))
            return render(
                request,
                'tables_app/cashouts.html', {
                    'table': table,
                    'profitsum': profitsum,
                    'lpsum': lpsum,
                    'uid': uid
                }
            )
        else:
            table = Cashout.objects.filter(client=request.user)
            profitsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('profit'))
            lpsum = Cashout.objects.filter(client=request.user).aggregate(total=Sum('lp'))
            return render(
                request,
                'tables_app/cashouts.html', {
                    'table': table,
                    'profitsum': profitsum,
                    'lpsum': lpsum,
                }
            )
