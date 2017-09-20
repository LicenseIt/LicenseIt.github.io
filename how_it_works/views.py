from django.shortcuts import render
from django.views import View


# Create your views here.
class HowItWorks(View):
    '''
    how it works page
    '''
    def get(self, request):
        '''
        how it works page
        :param request: request object
        :return: the page
        '''
        return render(request, 'how_it_works/works.html', context={'url': 'works'})
