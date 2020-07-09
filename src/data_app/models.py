from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


def json_default():
    return {
        "": 0
    }


def store_choices():
    return [
        ('Guristas', 'Guristas'),
        ('Sanshas', 'Sanshas'),
        ('DED', 'DED'),
        ('None', 'None')
    ]


class Cashout(models.Model):
    """Holds values from each client lp cashout."""

    cashout_id = models.IntegerField(
        primary_key=True,
        verbose_name='Cashout ID'
    )
    client = models.CharField(max_length=100)
    date = models.DateField()
    lp = models.IntegerField(verbose_name='LP')
    rate = models.IntegerField()
    profit = models.BigIntegerField()
    lp_type = models.CharField(
        choices=store_choices(),
        max_length=100,
        verbose_name='LP Type'
    )
    items = JSONField(default=json_default)

    class Meta:
        ordering = ['-cashout_id']
        verbose_name = 'LP Cashout'

    def save(self, *args, **kwargs):
        # Calculates the profit field on save
        self.profit = (self.lp * self.rate)

        super(Cashout, self).save(*args, **kwargs)
