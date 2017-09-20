from django.shortcuts import render
from django.views import View


# Create your views here.
class Faq(View):
    '''
    FAQ page
    '''
    def get(self, request):
        '''
        faq page
        :param request: request object
        :return: faq page
        '''
        return render(request, 'faq/faq.html', context={'url': 'faq'})
