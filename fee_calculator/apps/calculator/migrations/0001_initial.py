# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvocateType',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='FeeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=20)),
                ('is_basic', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='OffenceClass',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_per_unit', models.DecimalField(decimal_places=3, max_digits=10)),
                ('limit_from', models.SmallIntegerField(default=1)),
                ('limit_to', models.SmallIntegerField(null=True)),
                ('advocate_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='calculator.AdvocateType')),
                ('fee_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='calculator.FeeType')),
                ('offence_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='calculator.OffenceClass')),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effective_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('suty_base_type', models.PositiveSmallIntegerField(choices=[(1, 'Advocate'), (2, 'Solicitor')])),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='scenario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='calculator.Scenario'),
        ),
        migrations.AddField(
            model_name='price',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='calculator.Scheme'),
        ),
        migrations.AddField(
            model_name='price',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='calculator.Unit'),
        ),
    ]
