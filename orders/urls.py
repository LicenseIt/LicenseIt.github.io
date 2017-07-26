from django.conf.urls import url
from .views import (
    OrderView,
    OrderListView,
    OrderAdView,
    OrderIndieView,
    OrderProgramView,
    OrderWeddingView
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('now/(?P<pk>[0-9]+)/ad/(?P<order_id>[0-9]+)/$', OrderAdView.as_view(), name='order_ad'),
    url('now/(?P<pk>[0-9]+)/indie/(?P<order_id>[0-9]+)/$', OrderIndieView.as_view(), name='order_indie'),
    url('now/(?P<pk>[0-9]+)/program/(?P<order_id>[0-9]+)/$', OrderProgramView.as_view(), name='order_program'),
    url('now/(?P<pk>[0-9]+)/wedding/(?P<order_id>[0-9]+)/$', OrderWeddingView.as_view(), name='order_wedding'),
    url('now/(?P<pk>[0-9]+)/$', OrderView.as_view(), name='order'),
    url('', OrderListView.as_view(), name='order_list'),
]
