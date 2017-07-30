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
