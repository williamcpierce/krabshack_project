from django.contrib import admin

from .models import EsiCharacter, EsiMarket


class EsiCharacterAdmin(admin.ModelAdmin):
    list_display = (
        'assoc_user',
        'character_name',
        'access_token_expires'
    )
    fields = [
        'assoc_user',
        'character_name',
        'character_id',
        'character_lp',
        'refresh_token',
        'access_token',
        'access_token_expires'
    ]


class EsiMarketAdmin(admin.ModelAdmin):
    radio_fields = {'lp_type': admin.VERTICAL}
    list_display = (
        'type_id',
        'type_name',
        'lp_type',
        'sell_order_min',
        'buy_order_max',
        'daily_volume',
        'daily_isk',
        'orders_last_updated',
        'history_last_updated'
    )
    fields = [
        'type_id',
        'type_name',
        'lp_type',
        'market_orders',
        'market_history',
        'orders_last_updated',
        'history_last_updated'
    ]


admin.site.register(EsiCharacter, EsiCharacterAdmin)
admin.site.register(EsiMarket, EsiMarketAdmin)
