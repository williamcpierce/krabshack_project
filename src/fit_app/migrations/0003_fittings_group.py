# Generated by Django 3.0.7 on 2020-07-12 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit_app', '0002_auto_20200712_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='fittings',
            name='group',
            field=models.CharField(blank=True, choices=[('Super Group', 'Super Group'), ('Cap Group', 'Cap Group'), ('Horde Vanguard.', 'Horde Vanguard.'), ('None', 'None')], max_length=100, null=True),
        ),
    ]
