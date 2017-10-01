from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import CreatePayment

urlpatterns = [
    url('^create-payment/(?P<order_id>[0-9]+)', login_required(CreatePayment.as_view()), name='create_payment'),
]
