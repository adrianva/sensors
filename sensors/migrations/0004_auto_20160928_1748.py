# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_auto_20160926_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
