from django.contrib import admin
from .models import Order, OrderAdvertising, OrderIndie
from .models import OrderProgram, OrderWedding
from .models import ProjectType

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderAdvertising)
admin.site.register(OrderIndie)
admin.site.register(OrderProgram)
admin.site.register(OrderWedding)
admin.site.register(ProjectType)
