# Generated by Django 2.2.5 on 2019-09-21 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables_app', '0009_auto_20190921_0147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cashout',
            old_name='id',
            new_name='cashout_id',
        ),
    ]