from django.shortcuts import render
from django.views.generic import View

from contact.forms import ContactForm


class IndexView(View):
    def get(self, request):
        form = ContactForm()
        return render(request,
                      'home/index.html',
                      context={'url': 'home', 'form': form})
