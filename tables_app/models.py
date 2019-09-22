from django.db import models
from django.contrib.postgres.fields import JSONField

def items_default():
    return {
        "": 0
    }

class Cashout(models.Model):
    """holds values from each client lp cashout"""
    store_choices = [
        ('Guristas', 'Guristas'),
        ('Guristas', 'Sanshas')
    ]
    cashout_id = models.IntegerField(primary_key=True)
    client = models.CharField(max_length=100)
    date = models.DateField()
    lp = models.IntegerField()
    rate = models.IntegerField()
    profit = models.BigIntegerField()
    lp_type = models.CharField(
	    choices=store_choices,
        max_length=100
    )
    items = JSONField(default=items_default)
