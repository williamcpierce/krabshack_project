from django.db import models


class LPRate(models.Model):
    lp_type = models.CharField(
    	primary_key=True,
    	max_length=100,
    	verbose_name="LP Type"
    )
    lp_rate = models.IntegerField(
    	verbose_name="LP Rate"
    )
    last_updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["lp_type"]
        verbose_name = "LP Rate"

class SiteContent(models.Model):
    field_id = models.CharField(
        primary_key=True,
        max_length=100,
        verbose_name="Field ID"
    )
    field_text = models.TextField()
    last_updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["field_id"]
        verbose_name = "Site Content"

class CourierRoute(models.Model):
    route_id = models.CharField(
        primary_key=True,
        max_length=100,
        verbose_name="Route ID"
    )
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    m3_pricing = models.IntegerField()
    collateral_percent = models.DecimalField(
        max_digits=3,
        decimal_places=1
    )
    max_volume = models.IntegerField()
    completion_days = models.IntegerField()
    last_updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["route_id"]
        verbose_name = "Courier Route"