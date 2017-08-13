from django.contrib import admin
from .models import AskUser, Notifications

# Register your models here.
admin.site.register(AskUser)
admin.site.register(Notifications)
