# Generated by Django 2.2.5 on 2019-09-21 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables_app', '0011_auto_20190921_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashout',
            name='lp_type',
            field=models.CharField(choices=[('Guristas', 'Guristas'), ('Guristas', 'Sanshas')], max_length=100),
        ),
    ]
