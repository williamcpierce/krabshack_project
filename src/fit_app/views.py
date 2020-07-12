import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .models import Fittings
from .util import compare, out, parse
from esi_app import util as esiutil


class FitFix(View):
    """."""

    @staticmethod
    def get(request):
        """."""
        if request.user.is_authenticated:
            character_id = request.user.social_auth.get().uid
            if esiutil.get_corp(character_id) == 98477766 or request.user.is_superuser:
                fittings = Fittings.objects.all()
        else:
            fittings = Fittings.objects.filter(group='None')

        return render(
            request,
            'fit_app/fit.html', {
                'fittings': fittings
            }
        )


    @staticmethod
    def post(request):
        """."""
        response_data = {}

        for form_input in json.loads(request.POST.get('inputs')):
            if form_input.get('name') == 'fit':
                fit = form_input.get('value')
            if form_input.get('name') == 'contents':
                input_fit = parse(form_input.get('value'))

        saved_fit = parse(Fittings.objects.get(name=fit).fitting)
        extra, required = compare(input_fit, saved_fit)

        response_data['extra'] = out(extra)
        response_data['required'] = out(required)

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
