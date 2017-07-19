from django.conf.urls import url
from .views import LoginView, SignupView, Account
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^login/', LoginView.as_view(), name='login'),
    url('^signup/', SignupView.as_view(), name='signup_page'),
    url('^my_account/$', Account.as_view(), name='my_account'),
]
