from django.shortcuts import render
from django.views import View


# Create your views here.
class HowItWorks(View):
    def get(self, request):
        return render(request, 'how_it_works/works.html', context={'url': 'works'})
