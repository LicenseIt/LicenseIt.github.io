from django.conf.urls import url
from .views import (
    OrderView,
    # OrderAdView,
    OrderIndieView,
    # OrderProgramView,
    # OrderWeddingView,
    # PersonalUseView
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # url('now/(?P<pk>[0-9]+)/ad/(?P<order_id>[0-9]+)/$', OrderAdView.as_view(), name='advertising'),
    url('now/(?P<pk>[0-9]+)/indie/(?P<order_id>[0-9]+)/$', OrderIndieView.as_view(), name='film_making'),
    # url('now/(?P<pk>[0-9]+)/program/(?P<order_id>[0-9]+)/$', OrderProgramView.as_view(), name='programming'),
    # url('now/(?P<pk>[0-9]+)/wedding/(?P<order_id>[0-9]+)/$', OrderWeddingView.as_view(), name='wedding'),
    # url('now/(?P<pk>[0-9]+)/personal/(?P<order_id>[0-9]+)/$', PersonalUseView.as_view(), name='personal_use'),
    url('now/(?P<pk>[0-9]+)/$', OrderView.as_view(), name='order'),
]
