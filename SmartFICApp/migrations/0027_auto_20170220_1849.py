# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-20 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0026_auto_20170220_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambiente1m',
            name='Humedad1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ambiente1m',
            name='Humedad2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ambiente1m',
            name='Temperatura1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ambiente1m',
            name='Temperatura2',
            field=models.IntegerField(null=True),
        ),
    ]
