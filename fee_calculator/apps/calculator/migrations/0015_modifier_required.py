# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0014_auto_20171016_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='modifier',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]
