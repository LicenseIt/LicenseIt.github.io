from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Order(models.Model):
    SENT = 'sent'
    DONE = 'done'
    ATTENTION = 'attention'

    ORDER_CHOICES = (
        (SENT, 'Sent'),
        (ATTENTION, 'Attention'),
        (DONE, 'Done'),
    )

    user = models.ForeignKey(User)
    state = models.CharField(max_length=20, choices=ORDER_CHOICES, default=SENT)
