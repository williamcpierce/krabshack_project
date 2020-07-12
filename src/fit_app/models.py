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

    class Meta:
        verbose_name = 'Fittings'
        verbose_name_plural = 'Fittings'
        ordering = ['ship']

    def __str__(self):
        return f'{self.name}'
