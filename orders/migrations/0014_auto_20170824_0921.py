# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_order_license_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='license_pdf',
            field=models.FileField(blank=True, null=True, upload_to=orders.models.license_path),
        ),
    ]