import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.
class Search(models.Model):
    search_term = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search_term


class Artist(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=400)
    artist = models.ForeignKey('Artist',
                               on_delete=models.CASCADE,
                               related_name='artist_collections')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name) + ', ' + str(self.artist)


class Track(models.Model):
    name = models.CharField(max_length=400)
    kind = models.CharField(max_length=400)
    collection = models.ForeignKey('Collection',
                                   on_delete=models.CASCADE,
                                   related_name='collection_tracks')
    artist = models.ForeignKey('Artist',
                               on_delete=models.CASCADE,
                               related_name='artist_tracks')
    search = models.ForeignKey('Search',
                               on_delete=models.CASCADE,
                               related_name='search_tracks')
    artwork_100 = models.URLField(null=True, blank=True)
    artwork_60 = models.URLField(null=True, blank=True)
    track_time = models.CharField(max_length=20)
    description = models.TextField(default='')
    genre_category = models.CharField(max_length=200, default='')
    release_date = models.DateField(default=datetime.date(1900, 1, 1))
    media_copyright = models.CharField(max_length=300, default='')
    preview_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'track: ' + str(self.name) + ', ' + str(self.artist)

    @property
    def get_time(self):
        time = int(self.track_time) // 1000
        return datetime.timedelta(seconds=time)
