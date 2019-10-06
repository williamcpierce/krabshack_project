from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from datetime import datetime, timezone, timedelta
from .esi import esi_app, esi_security, esi_client
from statistics import mean
from decimal import Decimal
import esi_app.util as util
import time
import json
import requests


def json_default():
    return {
        "": 0
    }

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
    character_lp = JSONField(default=json_default)
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

    def update_lp(self):
        # esi call for lp values
        esi_response = esi_app.op['get_characters_character_id_loyalty_points'](
            character_id=self.character_id
        )
        self.character_lp = esi_client.request(esi_response).data

        # saves character
        self.save()


class EsiMarket(models.Model):
    store_choices = [
        ('Guristas', 'Guristas'),
        ('Sanshas', 'Sanshas'),
        ('None', 'None')
    ]
    type_id = models.IntegerField(
        primary_key=True,
        verbose_name='Type ID'
    )
    type_name = models.CharField(max_length=200)
    market_orders = JSONField(default=json_default)
    sell_order_min = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    buy_order_max = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    market_history = JSONField(default=json_default)
    daily_volume = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    daily_isk = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    lp_type = models.CharField(
        choices=store_choices,
        max_length=100,
        verbose_name='LP Type'
    )
    orders_last_updated = models.DateTimeField()
    history_last_updated = models.DateTimeField()

    class Meta:
        ordering = ['type_id']
        verbose_name = 'Market Data'
        verbose_name_plural = 'Market Data'

    def update_orders(self, *args, **kwargs):
        if self.orders_last_updated < datetime.now(timezone.utc)-timedelta(days=1):
            esi_response = requests.get(
                'https://esi.evetech.net/latest/markets/'+
                str(10000002)+
                '/orders/?order_type=all&type_id='+
                str(self.type_id)
            )
            if esi_response.status_code == 200:
                self.market_orders = esi_response.json()
                parsed_data = util.parse_market_orders(self.market_orders)
                self.sell_order_min = parsed_data['sell_order_min']
                self.buy_order_max = parsed_data['buy_order_max']
                self.orders_last_updated = datetime.now(timezone.utc)
                self.update_daily_isk()

        super(EsiMarket, self).save(*args, **kwargs)

    def update_history(self, *args, **kwargs):
        if self.history_last_updated < datetime.now(timezone.utc)-timedelta(days=7):
            esi_response = requests.get(
                'https://esi.evetech.net/latest/markets/'+
                str(10000002)+
                '/history/?&type_id='+
                str(self.type_id)
            )
            if esi_response.status_code == 200:
                self.market_history = esi_response.json()
                self.daily_volume = util.parse_market_history(self.market_history)
                self.history_last_updated = datetime.now(timezone.utc)
                self.update_daily_isk()

        super(EsiMarket, self).save(*args, **kwargs)

    def update_daily_isk(self, *args, **kwargs):
        self.daily_isk = self.daily_volume * Decimal(self.sell_order_min)

        super(EsiMarket, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.update_orders()
        self.update_history()
        self.update_daily_isk()

        super(EsiMarket, self).save(*args, **kwargs)

