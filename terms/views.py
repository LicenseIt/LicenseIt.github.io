from django.shortcuts import render
from django.views import View


# Create your views here.
class Terms(View):
    '''
    terms page
    '''
    def get(self, request):
        '''
        the terms page
        :param request: request object
        :return: terms page
        '''
        return render(request, 'terms/terms.html', context={'url': 'terms'})
