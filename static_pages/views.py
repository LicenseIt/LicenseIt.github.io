from django.shortcuts import render
from django.views import View


# Create your views here.
class LPYoutubeView(View):
    def get(self, request):
        return render(request, 'static_pages/index.html')
