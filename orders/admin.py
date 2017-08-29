from django.contrib import admin
from django.core.mail import send_mail

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
class MailChangeStatus(admin.ModelAdmin):
    list_display = ['user', 'song_title', 'state', 'project_type']
    actions = ['update_status_user']

    def update_status_user(self, request, queryset):
        for order in queryset.all():
            send_mail('licenseit- your order status has changed',
                      'your order status has changed to {0}. you can check it at {1}/accounts/my_account/'
                      .format(order.state, request.get_host()),
                      'cdo@licenseit.net',
                      [order.user.email])

    update_status_user.short_description = 'send email to update on status'


admin.site.register(Order, MailChangeStatus)
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
