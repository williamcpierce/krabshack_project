# Generated by Django 2.2 on 2019-04-04 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esicharacter',
            name='access_token_expires',
            field=models.DateTimeField(),
        ),
    ]
