# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-20 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0032_ambiente1m_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambiente1m',
            name='Humedad1',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ambiente1m',
            name='Humedad2',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ambiente1m',
            name='Temperatura1',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ambiente1m',
            name='Temperatura2',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
