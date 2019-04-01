from django.shortcuts import render


def couriers(request):
    if request.user.is_authenticated:
        uid = request.user.social_auth.get(provider='eveonline').uid
        return render(
            request,
            'site_app/couriers.html', {
                'uid': uid
            }
        )
    else:
        return render(request, 'site_app/couriers.html')


def buyback(request):
    if request.user.is_authenticated:
        uid = request.user.social_auth.get(provider='eveonline').uid
        return render(
            request,
            'site_app/buyback.html', {
                'uid': uid
            }
        )
    else:
        return render(request, 'site_app/buyback.html')


def home(request):
    if request.user.is_authenticated:
        uid = request.user.social_auth.get(provider='eveonline').uid
        return render(
            request,
            'site_app/home.html', {
                'uid': uid
            }
        )
    else:
        return render(request, 'site_app/home.html')
