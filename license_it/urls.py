"""license_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
# from django.contrib.auth.decorators import login_required, permission_required

from about.views import AboutView
from how_it_works.views import HowItWorks
from contact.views import ContactUs

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^search/', include('search.urls')),
    url('^accounts/', include('accounts.urls')),
    url('^order/', include('orders.urls')),
    url('^about/', AboutView.as_view(), name='about'),
    url('^how_it_works/', HowItWorks.as_view(), name='how_it_works'),
    url('^contact/', ContactUs.as_view(), name='contact_us'),
    url('', include('home.urls')),
]
