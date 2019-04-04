# Generated by Django 2.2 on 2019-04-04 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EsiCharacter',
            fields=[
                ('character_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('character_owner_hash', models.CharField(max_length=255)),
                ('character_name', models.CharField(max_length=200)),
                ('access_token', models.CharField(max_length=4096)),
                ('access_token_expires', models.DateField(max_length=4096)),
                ('refresh_token', models.CharField(max_length=200)),
            ],
        ),
    ]