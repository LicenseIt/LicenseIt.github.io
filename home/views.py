from django.shortcuts import render
from django.views.generic import View

from contact.forms import ContactForm


class IndexView(View):
    '''
    home page
    '''
    def get(self, request):
        '''
        home page
        :param request: request object
        :return: home page
        '''
        form = ContactForm()
        return render(request,
                      'home/index.html',
                      context={'url': 'home', 'form': form})
