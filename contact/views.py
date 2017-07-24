from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from .forms import ContactForm


# Create your views here.
class ContactUs(View):
    def get(self, request):
        form = ContactForm()
        return render(request,
                      'contact/contact.html',
                      context={'url': 'contact', 'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        return HttpResponse('error')
