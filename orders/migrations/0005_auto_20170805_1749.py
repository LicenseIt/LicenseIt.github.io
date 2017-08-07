# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_track_preview_url'),
        ('orders', '0004_auto_20170805_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.Track'),
        ),
        migrations.AlterField(
            model_name='orderadvertisingdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details_orderadvertisingdetail', to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='orderindieprojectdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details_orderindieprojectdetail', to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='orderprogrammingdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details_orderprogrammingdetail', to='orders.Order'),
        ),
    ]
