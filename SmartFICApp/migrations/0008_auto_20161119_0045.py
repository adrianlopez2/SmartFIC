# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 00:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0007_auto_20161117_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbienteP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('Temperatura', models.IntegerField()),
                ('Humedad', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Ambiente',
        ),
    ]
