from django.conf.urls import url
from .views import LoginView, SignupView, Account
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^login/', LoginView.as_view(), name='login'),
    url('^signup/', SignupView.as_view(), name='signup_page'),
    url('^my_account/order/(?P<order_id>[0-9]+)/', login_required(Account.as_view()), name='my_account_order'),
    url('^my_account/', login_required(Account.as_view()), name='my_account'),
]
