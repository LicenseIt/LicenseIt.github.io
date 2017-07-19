from django.contrib import admin
from .models import Search, Artist, Collection, Track

# Register your models here.
admin.site.register(Search)
admin.site.register(Artist)
admin.site.register(Collection)
admin.site.register(Track)
