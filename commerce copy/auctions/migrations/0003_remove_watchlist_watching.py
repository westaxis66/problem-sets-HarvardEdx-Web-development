# Generated by Django 3.2.5 on 2021-08-18 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_watchlist_watching'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='watching',
        ),
    ]
