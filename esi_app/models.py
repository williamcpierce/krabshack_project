from django.db import models

import time
from datetime import datetime, timezone


class EsiCharacter(models.Model):
    character_id = models.CharField(max_length=200, primary_key=True)
    character_owner_hash = models.CharField(max_length=255)
    character_name = models.CharField(max_length=200)
    access_token = models.CharField(max_length=4096)
    access_token_expires = models.DateTimeField()
    refresh_token = models.CharField(max_length=200)
    assoc_user = models.CharField(max_length=200, verbose_name='Owner')

    class Meta:
        ordering = ["assoc_user"]
        verbose_name = "Character"

    def get_id(self):
        # helper function to return character id
        return self.character_id

    def get_sso_data(self):
        # helper function to format input to esi_security.update_token
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': (
                self.access_token_expires - datetime.now(timezone.utc)
            ).total_seconds()
        }

    def update_token(self, token_response):
        # called when initializing/updating stored token values
        self.access_token = token_response['access_token']
        access_token_expiry = datetime.fromtimestamp(time.time() + token_response['expires_in'])
        # adds tz to time
        access_token_expiry_tz = access_token_expiry.replace(tzinfo=timezone.utc)
        self.access_token_expires = access_token_expiry_tz
        if 'refresh_token' in token_response:
            self.refresh_token = token_response['refresh_token']
        self.save()
