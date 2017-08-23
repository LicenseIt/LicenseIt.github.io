from django.conf import settings
from django.db import models

from orders.models import Order


class AskUser(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.TextField(null=True, blank=True)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='questions_on_order')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PersonalInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='user_info')
    address = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UserImage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='user_image')
    image_url = models.URLField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Notifications(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('question', 'question'),
        ('state', 'state'),
    )
    notification_type = models.CharField(max_length=20,
                                         choices=NOTIFICATION_TYPE_CHOICES)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='notifications_for_order')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_notifications')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
