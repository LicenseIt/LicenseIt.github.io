from django.conf.urls import url
from .views import OrderView, OrderListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^now/(?P<pk>[0-9]+)/$', OrderView.as_view(), name='order'),
    url('^$', OrderListView.as_view(), name='order_list'),
]
