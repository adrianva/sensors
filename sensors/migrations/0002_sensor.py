# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
    ]
