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
    list_display = ['id', 'user', 'song_title', 'state', 'project_type', 'created', 'updated']
    actions = ['update_status_user',
               'received_bid',
               'received_question',
               'received_answer']

    def update_status_user(self, request, queryset):
        for order in queryset.all():
            send_mail('licenseit- your order status has changed',
                      'your order status has changed to {0}. you can check it at {1}/accounts/my_account/'
                      .format(order.state, request.get_host()),
                      'cdo@licenseit.net',
                      [order.user.email],
                      html_message='')

    def received_bid(self, request, queryset):
        for order in queryset.all():
            send_mail('licenseit- your order status has changed',
                      'your order status has changed to {0}. you can check it at {1}/accounts/my_account/'
                      .format(order.state, request.get_host()),
                      'cdo@licenseit.net',
                      [order.user.email],
                      html_message='')

    def received_question(self, request, queryset):
        for order in queryset.all():
            send_mail('licenseit- your order status has changed',
                      'your order received a question. you can check it at {0}/accounts/my_account/'
                      .format(request.get_host()),
                      'cdo@licenseit.net',
                      [order.user.email],
                      html_message='')

    def received_answer(self, request, queryset):
        for order in queryset.all():
            send_mail('licenseit- your order status has changed',
                      'your order received an answer. you can check it at {0}/accounts/my_account/'
                      .format(request.get_host()),
                      'cdo@licenseit.net',
                      [order.user.email],
                      html_message='')

    update_status_user.short_description = 'send email to update on status'
    received_bid.short_description = 'send email to received bid'
    received_question.short_description = 'send email to received question'
    received_answer.short_description = 'send email to received answer'


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
