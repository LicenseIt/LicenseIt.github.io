from django.shortcuts import render
from django.views import View


# Create your views here.
class Terms(View):
    def get(self, request):
        return render(request, 'terms/terms.html', context={'url': 'terms'})
