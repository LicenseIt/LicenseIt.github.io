from django import template

from accounts.models import Notifications, UserImage

register = template.Library()


@register.simple_tag(is_safe=True)
def user_image(user):
    return '<img src="{0}" alt="user image" width=40 height=40>'.format(UserImage.objects.get(user=user).image_url)
