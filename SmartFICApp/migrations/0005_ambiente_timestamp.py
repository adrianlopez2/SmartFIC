# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-16 09:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0004_remove_ambiente_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambiente',
            name='Timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
