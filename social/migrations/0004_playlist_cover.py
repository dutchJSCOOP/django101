# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-12 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20160310_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
