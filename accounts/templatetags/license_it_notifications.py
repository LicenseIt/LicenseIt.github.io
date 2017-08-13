from django import template

from accounts.models import Notifications

register = template.Library()


@register.simple_tag
def notifications(user):
    return Notifications.objects.filter(user=user).count()
