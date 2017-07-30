from django.contrib import admin
from .models import (
    Order,
    WebEntries,
    ExternalEntries,
    OrderDistributionProgramming,
    OrderDistributionIndie,
    WebDistribution,
    ExternalDistribution,
    TvDistribution,
    OrderFilmMaking,
    OrderWedding,
    OrderAdvertising,
    OrderPersonal,
    OrderProgramming,
    OrderAdvertisingDetails,
    OrderIndieProjectDetails,
    OrderProgrammingDetails
)
from .models import ProjectType

# Register your models here.
admin.site.register(Order)
admin.site.register(WebEntries)
admin.site.register(ExternalEntries)
admin.site.register(OrderDistributionProgramming)
admin.site.register(OrderDistributionIndie)
admin.site.register(WebDistribution)
admin.site.register(ExternalDistribution)
admin.site.register(TvDistribution)
admin.site.register(OrderFilmMaking)
admin.site.register(OrderWedding)
admin.site.register(OrderAdvertising)
admin.site.register(OrderPersonal)
admin.site.register(OrderProgramming)
admin.site.register(OrderAdvertisingDetails)
admin.site.register(OrderIndieProjectDetails)
admin.site.register(OrderProgrammingDetails)
admin.site.register(ProjectType)
