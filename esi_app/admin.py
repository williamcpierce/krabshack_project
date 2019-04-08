from django.contrib import admin
from .models import EsiCharacter


class ESIAdmin(admin.ModelAdmin):
    list_display = (
        'assoc_user',
        'character_name',
        'access_token_expires'
    )
    fields = [
        'assoc_user',
        'character_name',
        'character_id',
        'refresh_token',
        'access_token',
        'access_token_expires'
    ]


admin.site.register(EsiCharacter, ESIAdmin)
