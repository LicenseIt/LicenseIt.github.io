from django.conf.urls import url
from .views import SearchView, ResultsView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^results/(?P<pk>[0-9]+)/$', login_required(ResultsView.as_view()), name='results_page'),
    url(r'', SearchView.as_view(), name='search_page'),
]
