# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-26 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0040_auto_20170322_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ajustes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Temperatura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Humedad', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]