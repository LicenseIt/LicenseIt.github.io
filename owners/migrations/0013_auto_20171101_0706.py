# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-01 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0012_auto_20171029_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderownerright',
            name='price',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]