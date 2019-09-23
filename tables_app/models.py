from django.db import models
from django.contrib.postgres.fields import JSONField

def items_default():
    return {
        "": 0
    }

def valuepull(valuedict, lookup):
    value = valuedict.get(lookup)
    if value is None:
        value = 0
    return value

class Cashout(models.Model):
    """holds values from each client lp cashout"""
    store_choices = [
        ('Guristas', 'Guristas'),
        ('Sanshas', 'Sanshas')
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

    def save(self, *args, **kwargs):
        lp = (
            valuepull(self.items, 'Gila Blueprint') * 80000 + 
            valuepull(self.items, 'Worm Blueprint') * 20000 + 
            valuepull(self.items, 'High-grade Crystal Alpha') * 23625 + 
            valuepull(self.items, 'High-grade Crystal Beta') * 31500 + 
            valuepull(self.items, 'High-grade Crystal Gamma') * 47250 + 
            valuepull(self.items, 'High-grade Crystal Delta') * 78750 + 
            valuepull(self.items, 'High-grade Crystal Epsilon') * 141750 + 
            valuepull(self.items, 'High-grade Crystal Omega') * 267750 + 
            valuepull(self.items, 'Mid-grade Crystal Alpha') * 7500 + 
            valuepull(self.items, 'Mid-grade Crystal Beta') * 10000 + 
            valuepull(self.items, 'Mid-grade Crystal Gamma') * 15000 + 
            valuepull(self.items, 'Mid-grade Crystal Delta') * 25000 + 
            valuepull(self.items, 'Mid-grade Crystal Epsilon') * 45000 + 
            valuepull(self.items, 'Mid-grade Crystal Omega') * 85000 + 
            valuepull(self.items, 'Succubus Blueprint') * 20000 + 
            valuepull(self.items, 'High-grade Amulet Alpha') * 23625 + 
            valuepull(self.items, 'High-grade Amulet Beta') * 31500 + 
            valuepull(self.items, 'High-grade Amulet Gamma') * 47250 + 
            valuepull(self.items, 'High-grade Amulet Delta') * 78750 + 
            valuepull(self.items, 'High-grade Amulet Epsilon') * 141750 + 
            valuepull(self.items, 'High-grade Amulet Omega') * 267750 + 
            valuepull(self.items, 'Mid-grade Amulet Alpha') * 7500 + 
            valuepull(self.items, 'Mid-grade Amulet Beta') * 10000 + 
            valuepull(self.items, 'Mid-grade Amulet Gamma') * 15000 + 
            valuepull(self.items, 'Mid-grade Amulet Delta') * 25000 + 
            valuepull(self.items, 'Mid-grade Amulet Epsilon') * 45000 + 
            valuepull(self.items, 'Mid-grade Amulet Omega') * 85000
            )
        self.lp = lp
        self.profit = (lp * self.rate)
        super(Cashout, self).save(*args, **kwargs)