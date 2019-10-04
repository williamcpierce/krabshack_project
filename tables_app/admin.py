from django.contrib import admin
from .models import Cashout


class CashoutAdmin(admin.ModelAdmin):
    radio_fields = {'lp_type': admin.VERTICAL}
    list_display = (
    	'cashout_id',
    	'date',
    	'client',
    	'lp',
    	'lp_type',
    	'rate',
    	'profit'
    )
    fields = [
    	'cashout_id',
    	'client',
    	'date',
    	'lp',
    	'lp_type',
    	'rate',
    	'items'
    ]
    list_filter = (
        'date',
        'lp_type'
    )
    search_fields = [
        'client',
        'cashout_id'
    ]


admin.site.register(Cashout, CashoutAdmin)
