# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20170805_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpersonal',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orderpersonal_details', to='orders.Order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderwedding',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orderwedding_details', to='orders.Order'),
            preserve_default=False,
        ),
    ]