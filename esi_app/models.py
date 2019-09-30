from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from datetime import datetime, timezone
import time
import esi_app.esi as esi


def lp_default():
    return {
        "": 0
    }


class EsiCharacter(models.Model):
    character_id = models.CharField(
        max_length=200,
        primary_key=True
    )
    character_owner_hash = models.CharField(max_length=255)
    character_name = models.CharField(max_length=200)
    character_lp = JSONField(default=lp_default)
    access_token = models.CharField(max_length=4096)
    access_token_expires = models.DateTimeField()
    refresh_token = models.CharField(max_length=200)
    assoc_user = models.ForeignKey(
        User,
        to_field='username',
        db_column='assoc_user',
        verbose_name='Owner',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['assoc_user']
        verbose_name = 'Character'

    def get_tokens(self):
        """
        helper function to format input to esi_security.update_token
        """
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': (
                self.access_token_expires - datetime.now(timezone.utc)
            ).total_seconds()
        }

    def update_tokens(self, token_response):
        """
        called when initializing/updating stored token values, distinct from esi_security.update_token
        """
        # saves access token and access token expiry with tz
        self.access_token = token_response['access_token']
        access_token_expiry = datetime.fromtimestamp(time.time() + token_response['expires_in'])
        access_token_expiry_tz = access_token_expiry.replace(tzinfo=timezone.utc)
        self.access_token_expires = access_token_expiry_tz
        
        # saves refresh token
        if 'refresh_token' in token_response:
            self.refresh_token = token_response['refresh_token']
        
        # saves character
        self.save()

    def update_data(self):
        # esi call for lp values
        esi_call = esi.esi_app.op['get_characters_character_id_loyalty_points'](
            character_id=self.character_id
        )
        self.character_lp = esi.esi_client.request(esi_call).data

        # saves character
        self.save()
