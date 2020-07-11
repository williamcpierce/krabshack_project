from django.db import models


class Fittings(models.Model):
    """."""

    # Model/database fields
    name = models.CharField(
        primary_key=True,
        max_length=100
    )
    ship = models.CharField(
        max_length=100
    )
    fitting = models.TextField()
