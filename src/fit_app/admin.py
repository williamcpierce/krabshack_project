from django.contrib import admin

from .models import Fittings



class FittingsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'ship',
    )


admin.site.register(Fittings, FittingsAdmin)
