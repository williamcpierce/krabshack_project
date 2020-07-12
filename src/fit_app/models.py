from django.db import models


def group_choices():
    return [
        ('Super Group', 'Super Group'),
        ('Cap Group', 'Cap Group'),
        ('Horde Vanguard.', 'Horde Vanguard.'),
        ('None', 'None')
   ]


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
    group = models.CharField(
        max_length=100,
        choices=group_choices(),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Fittings'
        verbose_name_plural = 'Fittings'
        ordering = ['ship']

    def __str__(self):
        return f'{self.name}'
