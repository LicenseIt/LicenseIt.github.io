import logging
import traceback

from django.db import IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import AskUser

from orders.models import Order
from orders.forms import OrderForm

from owners.models import Question, OwnerDatabase



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
    def get(self, request, order_id=None):
        orders_list = Order.objects.filter(user=request.user).select_related()
        owners = OwnerDatabase.objects.all()

        if order_id:
            order_data = Order.objects.get(pk=order_id)
        else:
            order_data = orders_list.first()

        if order_data:
            ask_user = AskUser.objects.filter(order=order_data.id)
        else:
            ask_user = ''

        context = {
            'url': 'client_dash',
            'orders_list': orders_list,
            'order_data': order_data,
            'ask_user': ask_user,
            'owners': owners,
        }

        if order_data and order_data.project_type.name == 'film making':
            order_details = order_data.order_details_orderindieprojectdetail.get(order=order_data.id)
            print(order_details.song_version)
            context['order_details'] = order_details
        if order_data and order_data.project_type.name == 'programming':
            order_details = order_data.order_details_orderprogrammingdetail.get(order=order_data.id)
            context['order_details'] = order_details
        elif order_data and order_data.project_type.name == 'advertising':
            order_details = order_data.order_details_orderadvertisingdetail.get(order=order_data.id)
            context['order_details'] = order_details

        return render(request,
                      'accounts/client-dash.html',
                      context=context)

    def post(self, request):
        pass
