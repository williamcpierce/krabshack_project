from django.db import models

class Rates(models.Model):
    lp_type = models.CharField(max_length=100)
    lp_rate = models.IntegerField()