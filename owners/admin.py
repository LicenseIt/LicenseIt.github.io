from django.contrib import admin

from .models import (
    OwnerDatabase,
    Question,
    RightType,
    OrderOwnerRight,
)


class OwnerRight(admin.ModelAdmin):
    list_display = ['owner', 'right_type', 'order']


# Register your models here.
admin.site.register(OwnerDatabase)
admin.site.register(Question)
admin.site.register(RightType)
admin.site.register(OrderOwnerRight, OwnerRight)
