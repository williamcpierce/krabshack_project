# Generated by Django 2.2.5 on 2019-10-21 16:01

from django.db import migrations, models
import esi_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('esi_app', '0002_esicharacter_character_bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esimarket',
            name='history_last_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='esimarket',
            name='orders_last_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
