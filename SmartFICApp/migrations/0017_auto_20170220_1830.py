# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-20 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0016_remove_ambiente_zona'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ambiente1m',
            name='Humedad',
        ),
        migrations.RemoveField(
            model_name='ambiente1m',
            name='Temperatura',
        ),
        migrations.AddField(
            model_name='ambiente1m',
            name='Humedad1',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ambiente1m',
            name='Humedad2',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ambiente1m',
            name='Temperatura1',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ambiente1m',
            name='Temperatura2',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
