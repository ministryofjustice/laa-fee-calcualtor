# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 14:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_remove_scenario_force_third'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='third',
        ),
    ]
