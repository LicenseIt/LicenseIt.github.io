from django.contrib import admin
from .models import AskUser, Notifications, UserImage

# Register your models here.
admin.site.register(AskUser)
admin.site.register(Notifications)
admin.site.register(UserImage)
