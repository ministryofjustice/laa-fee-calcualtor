# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 13:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0010_auto_20171011_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheme',
            name='effective_date',
        ),
    ]
