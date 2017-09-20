from django.shortcuts import render
from django.views import View


# Create your views here.
class Pricing(View):
    '''
    pricing page
    '''
    def get(self, request):
        '''
        pricing page
        :param request: request object
        :return: pricing page
        '''
        return render(request, 'pricing/pricing.html', context={'url': 'pricing'})
