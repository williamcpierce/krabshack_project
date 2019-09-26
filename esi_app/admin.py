from django.contrib import admin
from .models import EsiCharacter


class ESICharacterAdmin(admin.ModelAdmin):
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


admin.site.register(EsiCharacter, ESICharacterAdmin)
