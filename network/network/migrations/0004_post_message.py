# Generated by Django 3.2.5 on 2021-12-30 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='message',
            field=models.TextField(default=None, max_length=240),
        ),
    ]