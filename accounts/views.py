import logging
import traceback

from django.db import IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('search'))
        else:
            return render(request, 'accounts/login.html', context={'error': 'username or password is wrong'})


class SignupView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
        except IntegrityError:
            return render(request, 'accounts/signup.html', context={'error': 'this username is already taken'})
        except:
            logger = logging.getLogger(__name__)
            logger.error('error in signup')
            logger.error(traceback.print_exc())
            logger.error('end traceback')
        return HttpResponseRedirect(reverse('search_page'))


class Account(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
