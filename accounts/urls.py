from django.conf.urls import url
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

from .views import (
    LoginView,
    SignupView,
    Account,
    LoginFacebook,
    EditUserData,
    ForgotPassword,
    ChangePassword,
)

urlpatterns = [
    url('^login/', LoginView.as_view(), name='login'),
    url('^signup/', SignupView.as_view(), name='signup_page'),
    url('^logout/', logout, {'next_page': '/'}, name='logout'),
    url('^forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    url('^(P<string>[A-z^]+)', ChangePassword.as_view(), name='change_password'),
    url('^edit_user/', login_required(EditUserData.as_view()), name='edit_user'),
    url('^facebook-login/(?P<email>[A-z@.]+)/(?P<url>[A-z:/.0-9_?=-]+)', LoginFacebook.as_view(), name='facebook_login'),
    url('^my_account/order/(?P<order_id>[0-9]+)/', login_required(Account.as_view()), name='my_account_order'),
    url('^my_account/', login_required(Account.as_view()), name='my_account'),
]
