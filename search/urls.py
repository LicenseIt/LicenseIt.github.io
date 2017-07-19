from django.conf.urls import url
from .views import SearchView, ResultsView

urlpatterns = [
    url(r'^results/(?P<pk>[0-9]+)/$', ResultsView.as_view(), name='results_page'),
    url(r'', SearchView.as_view(), name='search_page'),
]
