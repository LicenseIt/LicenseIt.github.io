# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-01 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20170920_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1.1, max_digits=10),
            preserve_default=False,
        ),
    ]