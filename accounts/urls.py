from django.conf.urls import url
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

from .views import LoginView, SignupView, Account, LoginFacebook

urlpatterns = [
    url('^login/', LoginView.as_view(), name='login'),
    url('^signup/', SignupView.as_view(), name='signup_page'),
    url('^logout/', logout, {'next_page': '/'}, name='logout'),
    url('^facebook-login/(?P<email>[A-z@.]+)', LoginFacebook.as_view(), name='facebook_login'),
    url('^my_account/order/(?P<order_id>[0-9]+)/', login_required(Account.as_view()), name='my_account_order'),
    url('^my_account/', login_required(Account.as_view()), name='my_account'),
]
