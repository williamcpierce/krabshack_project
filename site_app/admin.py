from django.contrib import admin
from .models import Rates

class RatesAdmin(admin.ModelAdmin):
    list_display = ('lp_type', 'lp_rate')
    fields = ['lp_type', 'lp_rate']


admin.site.register(Rates, RatesAdmin)