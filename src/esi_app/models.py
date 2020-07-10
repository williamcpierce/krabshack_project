from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json
import time

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
import esi_app.util as util
import requests

from .esi import esi_app, esi_security, esi_client


def json_default():
    return {
        "": 0
    }


def datetime_default():
    return datetime.now(timezone.utc)


def store_choices():
    return [
        ('Guristas', 'Guristas'),
        ('Sanshas', 'Sanshas'),
        ('Blood Raiders', 'Blood Raiders'),
        ('DED', 'DED'),
        ('None', 'None')
    ]


class EsiCharacter(models.Model):
    character_id = models.CharField(
        max_length=200,
        primary_key=True
    )
    character_owner_hash = models.CharField(max_length=255)
    character_name = models.CharField(max_length=200)
    character_lp = JSONField(default=json_default)
    character_bookmarks = JSONField(default=json_default)
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
        """Helper function to format input to esi_security.update_token."""

        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': (
                self.access_token_expires - datetime.now(timezone.utc)
            ).total_seconds()
        }

    def update_tokens(self, token_response):
        """Called when initializing/updating stored token values, distinct from esi_security.update_token."""

        # Saves access token and access token expiry with tz
        self.access_token = token_response['access_token']
        access_token_expiry = datetime.fromtimestamp(time.time() + token_response['expires_in'])
        access_token_expiry_tz = access_token_expiry.replace(tzinfo=timezone.utc)
        self.access_token_expires = access_token_expiry_tz

        # Saves refresh token
        if 'refresh_token' in token_response:
            self.refresh_token = token_response['refresh_token']

        # Saves character
        self.save()

    def update_lp(self):
        """Esi call for lp values."""

        esi_response = esi_app.op['get_characters_character_id_loyalty_points'](
            character_id=self.character_id
        )
        self.character_lp = esi_client.request(esi_response).data

        # Saves character
        self.save()

    def bookmarks(self):
        """Esi call for bookmark values."""

        esi_response = esi_app.op['get_characters_character_id_bookmarks'](
            character_id=self.character_id
        )
        character_bookmarks = esi_client.request(esi_response).data

        return character_bookmarks

    def structure_search(self, search_string):
        esi_response = esi_app.op['get_characters_character_id_search'](
            character_id=self.character_id,
            search=search_string,
            categories=['structure']
        )
        response_data = esi_client.request(esi_response).data

        return response_data

    def structure_info(self, structure):
        structure_int = structure[0]
        esi_response = esi_app.op['get_universe_structures_structure_id'](
            structure_id=structure_int
        )
        response_data = esi_client.request(esi_response).data

        return response_data


class EsiMarket(models.Model):
    type_id = models.IntegerField(
        primary_key=True,
        verbose_name='Type ID'
    )
    type_name = models.CharField(max_length=200)
    market_orders = JSONField(default=json_default)
    sell_order_min = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    buy_order_max = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    market_history = JSONField(default=json_default)
    daily_volume = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    daily_isk = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    lp_type = models.CharField(
        choices=store_choices(),
        max_length=100,
        verbose_name='LP Type',
        default='None'
    )
    orders_last_updated = models.DateTimeField(
        null=True,
        blank=True
    )
    history_last_updated = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['type_id']
        verbose_name = 'Market Data'
        verbose_name_plural = 'Market Data'

    def update_orders(self, *args, **kwargs):
        """Updates and parses market orders for an item, if older than 1 day."""

        # Only updates orders if more than 1 day old
        if self.orders_last_updated == None or self.orders_last_updated < datetime.now(timezone.utc)-timedelta(hours=1):
            esi_response = util.esi_request(
                op='orders',
                region_id=10000002,
                type_id=self.type_id,
                order_type='all'
            )

            # Only updates if response is good
            if esi_response.status_code == 200:
                self.market_orders = esi_response.json()
                parsed_data = util.parse_market_orders(self.market_orders)
                self.sell_order_min = parsed_data['sell_order_min']
                self.buy_order_max = parsed_data['buy_order_max']
                self.orders_last_updated = datetime.now(timezone.utc)
                self.update_daily_isk()

        super(EsiMarket, self).save(*args, **kwargs)

    def update_history(self, *args, **kwargs):
        """Updates and parses market history for an item, if older than 1 day."""

        # Only updates history if more than 1 day old
        if self.history_last_updated == None or self.history_last_updated < datetime.now(timezone.utc)-timedelta(days=1):
            esi_response = util.esi_request(
                op='history',
                region_id=10000002,
                type_id=self.type_id,
            )

            # Only updates if response is good
            if esi_response.status_code == 200:

                # If history is the default value, only sorts
                if self.market_history == json_default():
                    self.market_history = util.sort_list(
                        esi_response.json()
                    )

                # If non default, appends and sorts
                else:
                    self.market_history = util.sort_list(
                        util.append_list(
                            esi_response.json(),
                            self.market_history
                        )
                    )
                self.daily_volume = util.parse_market_history(self.market_history)
                self.history_last_updated = datetime.now(timezone.utc)
                self.update_daily_isk()

        super(EsiMarket, self).save(*args, **kwargs)

    def update_daily_isk(self, *args, **kwargs):
        """Calculates the daily isk volume of an item."""

        self.daily_isk = Decimal(self.daily_volume) * Decimal(self.sell_order_min)

        super(EsiMarket, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.update_orders()
        self.update_history()
        self.update_daily_isk()

        super(EsiMarket, self).save(*args, **kwargs)
