from django.db import models


class Cashout(models.Model):
    # holds values from each client lp cashout
    client = models.CharField(max_length=100)
    date = models.DateField()
    lp = models.IntegerField()
    rate = models.IntegerField()
    profit = models.IntegerField()
