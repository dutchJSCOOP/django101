# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20160317_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='savedBy',
        ),
    ]
