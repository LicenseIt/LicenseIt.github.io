from django import template

from accounts.models import Notifications, UserImage

register = template.Library()


@register.simple_tag(is_safe=True)
def user_image(user):
    return UserImage.objects.get(user=user).image_url
