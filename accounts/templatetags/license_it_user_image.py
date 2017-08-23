from django import template

from accounts.models import Notifications, UserImage

register = template.Library()


@register.simple_tag
def user_image(user):
    return '<img src="{0}" alt="user image">'.format(UserImage.objects.get(user=user).image_url)
