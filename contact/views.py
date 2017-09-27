from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from .forms import ContactForm


# Create your views here.
class ContactUs(View):
    '''
    contact us view
    '''
    def get(self, request):
        '''
        contact us page
        :param request: request object
        :return: contact us page
        '''
        form = ContactForm()
        return render(request,
                      'contact/contact.html',
                      context={'url': 'contact', 'form': form})

    def post(self, request):
        '''
        saving the contact us data
        :param request: request object
        :return: success on success, error otherwise
        '''
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        return HttpResponse('error')
