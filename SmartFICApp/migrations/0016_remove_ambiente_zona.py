# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-16 17:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFICApp', '0015_remove_ambiente2_zona'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ambiente',
            name='Zona',
        ),
    ]
