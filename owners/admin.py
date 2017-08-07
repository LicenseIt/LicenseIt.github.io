from django.contrib import admin

from .models import OwnerDatabase, Question

# Register your models here.
admin.site.register(OwnerDatabase)
admin.site.register(Question)
