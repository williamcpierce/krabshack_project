from django.contrib import admin
from .models import Cashout


class CashoutAdmin(admin.ModelAdmin):
    list_display = ('cashout_id', 'date', 'client', 'lp', 'lp_type', 'rate', 'profit')
    fields = ['cashout_id', 'client', 'date', 'lp', 'lp_type','rate', 'profit', 'items']


admin.site.register(Cashout, CashoutAdmin)