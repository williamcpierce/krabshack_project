# Generated by Django 2.2.5 on 2019-09-20 21:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables_app', '0005_auto_20190920_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemlist',
            name='items',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
            preserve_default=False,
        ),
    ]