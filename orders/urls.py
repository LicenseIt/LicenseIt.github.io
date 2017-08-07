from django.conf.urls import url
from .views import (
    OrderView,
    OrderIndieView,
    OrderProgramView,
    OrderAdvertisingView,
    AdvertisingDistribution,
    IndieDistribution,
    ProgramDistribution,
    ProgramDetail,
    IndieDetail,
    AdvertisingDetail,
    WeddingDetails,
    PersonalDetails,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('now/ad/(?P<order_id>[0-9]+)/$', OrderAdvertisingView.as_view(), name='advertising'),
    url('now/indie/(?P<order_id>[0-9]+)/distribution/$', IndieDistribution.as_view(), name='indie_dist'),
    url('now/program/(?P<order_id>[0-9]+)/distribution/$', ProgramDistribution.as_view(), name='prog_dist'),
    url('now/ad/(?P<order_id>[0-9]+)/distribution/$', AdvertisingDistribution.as_view(), name='ad_dist'),
    url('now/indie/(?P<order_id>[0-9]+)/details/$', IndieDetail.as_view(), name='indie_details'),
    url('now/program/(?P<order_id>[0-9]+)/details/$', ProgramDetail.as_view(), name='program_details'),
    url('now/ad/(?P<order_id>[0-9]+)/details/$', AdvertisingDetail.as_view(), name='advertising_details'),
    url('now/indie/(?P<order_id>[0-9]+)/$', OrderIndieView.as_view(), name='film_making'),
    url('now/program/(?P<order_id>[0-9]+)/$', OrderProgramView.as_view(), name='programming'),
    url('now/wedding/(?P<order_id>[0-9]+)/$', WeddingDetails.as_view(), name='wedding'),
    url('now/personal/(?P<order_id>[0-9]+)/$',  PersonalDetails.as_view(), name='personal_use'),
    url('now/(?P<song_id>[0-9]+)/$', OrderView.as_view(), name='order'),
    url('now/manual/$', OrderView.as_view(), name='manual_order'),
]
