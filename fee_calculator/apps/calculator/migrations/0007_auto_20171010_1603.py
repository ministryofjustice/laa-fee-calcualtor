# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 16:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('calculator', '0006_auto_20171005_1148'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Uplift',
            new_name='Modifier',
        ),
    ]
