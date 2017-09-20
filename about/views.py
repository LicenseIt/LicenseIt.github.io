from django.shortcuts import render
from django.views import View


# Create your views here.
class AboutView(View):
    '''
    class to handle all the http methods of the about page.
    '''
    def get(self, request):
        '''
        show the about page.
        :param request: the request object
        :return: the about page
        '''
        return render(request, 'about/about.html', context={'url': 'about'})
