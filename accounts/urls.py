from django.conf.urls import url
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

from .views import (
    LoginView,
    SignupView,
    Account,
    EditUserData,
    ForgotPassword,
    ChangePassword,
    CounterOfferView,
)

urlpatterns = [
    url('^login/', LoginView.as_view(), name='login'),
    url('^signup/', SignupView.as_view(), name='signup_page'),
    url('^logout/', logout, {'next_page': '/'}, name='logout'),
    url('^forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    url('^change_password/(?P<string>[A-z]+)/', ChangePassword.as_view(), name='change_password'),
    url('^edit_user/', login_required(EditUserData.as_view()), name='edit_user'),
    url('^counter-offer/(?P<order_id>[0-9]+)/', login_required(CounterOfferView.as_view()), name='counter_offer'),
    url('^counter-offer/', login_required(CounterOfferView.as_view()), name='counter_offer'),
    url('^my_account/order/(?P<order_id>[0-9]+)/', login_required(Account.as_view()), name='my_account_order'),
    url('^my_account/', login_required(Account.as_view()), name='my_account'),
]
