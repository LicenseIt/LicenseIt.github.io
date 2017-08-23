from django import template

from accounts.models import Notifications, UserImage

register = template.Library()


@register.simple_tag
def user_image(user):
    try:
        return UserImage.objects.get(user=user).image_url
    except UserImage.DoesNotExist:
        return ''
