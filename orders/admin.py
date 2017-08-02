from django.contrib import admin
from .models import (
    Order,
    WebEntry,
    ExternalEntry,
    OrderDistributionProgramming,
    OrderDistributionIndie,
    WebDistribution,
    FeaturedBackground,
    ExternalDistribution,
    TvDistribution,
    OrderFilmMaking,
    OrderWedding,
    OrderAdvertising,
    OrderPersonal,
    OrderProgramming,
    OrderAdvertisingDetail,
    OrderIndieProjectDetail,
    OrderProgrammingDetail
)
from .models import ProjectType

# Register your models here.
admin.site.register(Order)
admin.site.register(WebEntry)
admin.site.register(ExternalEntry)
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
admin.site.register(OrderAdvertisingDetail)
admin.site.register(OrderIndieProjectDetail)
admin.site.register(OrderProgrammingDetail)
admin.site.register(ProjectType)
admin.site.register(FeaturedBackground)
