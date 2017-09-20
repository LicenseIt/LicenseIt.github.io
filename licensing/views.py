from django.shortcuts import render
from django.views import View


# Create your views here.
class Licensing(View):
    '''
    licensing page
    '''
    def get(self, request):
        '''
        licensing page
        :param request: request object
        :return: licensing page
        '''
        return render(request, 'licensing/licensing.html')
