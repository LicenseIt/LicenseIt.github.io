# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 09:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_collections', to='search.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_term', models.CharField(max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('kind', models.CharField(max_length=400)),
                ('artwork_100', models.URLField(blank=True, null=True)),
                ('artwork_60', models.URLField(blank=True, null=True)),
                ('track_time', models.CharField(max_length=20)),
                ('description', models.TextField(default='')),
                ('genre_category', models.CharField(default='', max_length=200)),
                ('release_date', models.DateField(default=datetime.date(1900, 1, 1))),
                ('media_copyright', models.CharField(default='', max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_tracks', to='search.Artist')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_tracks', to='search.Collection')),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_tracks', to='search.Search')),
            ],
        ),
    ]
