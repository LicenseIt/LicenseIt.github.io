from django.shortcuts import render
from django.views import View


# Create your views here.
class Pricing(View):
    def get(self, request):
        return render(request, 'pricing/pricing.html', context={'url': 'pricing'})
