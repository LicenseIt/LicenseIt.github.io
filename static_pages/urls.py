from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'lpyoutube/$', LPYoutubeView.as_view()),
]
