# Generated by Django 2.2 on 2022-07-29 04:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20220729_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 29, 4, 41, 25, 224780, tzinfo=utc)),
        ),
    ]
