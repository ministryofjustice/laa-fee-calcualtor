# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0018_modifier_strict_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
