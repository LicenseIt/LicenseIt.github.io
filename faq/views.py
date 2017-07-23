from django.shortcuts import render
from django.views import View


# Create your views here.
class Faq(View):
    def get(self, request):
        return render(request, 'faq/faq.html', context={'url': 'faq'})
