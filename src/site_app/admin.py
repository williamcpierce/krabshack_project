from django.contrib import admin
from .models import LPRate, SiteContent, CourierRoute


class LPRateAdmin(admin.ModelAdmin):
    list_display = (
        'lp_type',
        'lp_rate',
        'last_updated'
    )
    fields = [
        'lp_type',
        'lp_rate'
    ]


class SiteContentAdmin(admin.ModelAdmin):
    list_display = (
        'field_id',
        'field_text',
        'last_updated'
    )
    fields = [
        'field_id',
        'field_text',
    ]


class CourierRouteAdmin(admin.ModelAdmin):
    list_display = (
        'route_id',
        'origin',
        'destination',
        'last_updated'
    )
    fields = [
        'route_id',
        'origin',
        'destination',
        'm3_pricing',
        'collateral_percent',
        'max_volume',
        'completion_days'
    ]


admin.site.register(LPRate, LPRateAdmin)
admin.site.register(SiteContent, SiteContentAdmin)
admin.site.register(CourierRoute, CourierRouteAdmin)
