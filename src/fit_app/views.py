import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Fittings


class FitFix(View):
    """."""

    @staticmethod
    def get(request):
        """."""

        return render(
            request,
            'fit_app/fit.html'
        )


    @staticmethod
    def post(request):
        """."""

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
