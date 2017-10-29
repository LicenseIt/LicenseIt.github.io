# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-29 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0011_auto_20171029_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderownerright',
            name='order',
            field=models.ForeignKey(default=88, on_delete=django.db.models.deletion.CASCADE, related_name='order_owner', to='orders.Order'),
            preserve_default=False,
        ),
    ]
