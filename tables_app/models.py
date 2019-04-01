from django.db import models


class Cashout(models.Model):
    client = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    lp = models.IntegerField()
    rate = models.IntegerField()
    profit = models.IntegerField()
