from django.contrib import admin
from .models import (
    AskUser,
    Notifications,
    UserImage,
    ResetPassword,
    CounterOffer,
    UserQuestion,
)


# Register your models here.
class CounterOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'order']


admin.site.register(AskUser)
admin.site.register(Notifications)
admin.site.register(UserImage)
admin.site.register(ResetPassword)
admin.site.register(CounterOffer, CounterOfferAdmin)
admin.site.register(UserQuestion)
