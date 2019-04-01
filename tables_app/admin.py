from django.contrib import admin
from .models import Cashout

# admin.site.register(Cashout)


class CashoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'client', 'lp', 'rate', 'profit')
    fields = ['client', 'date', ('lp', 'rate', 'profit')]


admin.site.register(Cashout, CashoutAdmin)
