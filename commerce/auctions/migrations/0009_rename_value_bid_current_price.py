# Generated by Django 3.2.5 on 2021-08-23 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210822_2047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='value',
            new_name='current_price',
        ),
    ]
