from django.contrib import admin
from .models import ContactData


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'created']


admin.site.register(ContactData, ContactAdmin)
