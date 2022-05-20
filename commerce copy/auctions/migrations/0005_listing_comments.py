# Generated by Django 3.2.5 on 2021-08-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist_watching'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments_in_listing', to='auctions.Comment'),
        ),
    ]
