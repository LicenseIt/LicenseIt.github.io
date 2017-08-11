import logging
import traceback

from django.db import IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from orders.models import Order
from owners.models import Question, OrderOwnerRight, OwnerDatabase
from common.helpers import generate_password

import sys
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from orders.forms import (
        OrderForm,
        OrderIndieForm,
        OrderProgramForm,
        OrderAdvertisingForm,
        IndieWebDistribution,
        IndieExtDistribution,
        TvDistributionForm,
        IndieDetailForm,
        ProgramDetailForm,
        AdvertisingDetailForm,
        WeddingDetailForm,
        PersonalDetailForm
    )


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
        return HttpResponseRedirect(reverse('search_page'))


class LoginFacebook(View):
    def post(self, request):
        email = request.POST['email']
        password = generate_password()
        try:
            user = User.objects.create_user(email, email, password)
            login(request, user)
            return HttpResponseRedirect(reverse(request.POST['url']))
        except IntegrityError:
            user = User.objects.get(username=email)
            login(request, user)
            return HttpResponseRedirect(reverse(request.POST['url']))


class Account(View):
    template_name = 'accounts/client-dash.html'

    def data(self, user, order_id=None):
        orders_list = Order.objects.filter(user=user).select_related()

        if order_id:
            order_data = Order.objects.get(pk=order_id)
        else:
            order_data = orders_list.first()

        if order_data:
            owners = OrderOwnerRight.objects.filter(order=order_data.id)
            ask_user = Question.objects.filter(order=order_data.id)
        else:
            ask_user = ''
            owners = ''

        context = {
            'url': 'client_dash',
            'orders_list': orders_list,
            'order_data': order_data,
            'order_form': OrderForm(instance=order_data),
            'ask_user': ask_user,
            'owners': owners,
        }

        if order_data and order_data.project_type.name.lower() == 'film making':
            indie_data = order_data.order_project_orderfilmmaking.get(order=order_data.id)
            context['indie_form'] = OrderIndieForm(instance=indie_data)
            details = order_data.order_details_orderindieprojectdetail.get(order=order_data.id)
            context['details_form'] = IndieDetailForm(instance=details)
            start = details.start_duration.split(':')
            end = details.end_duration.split(':')
            context['min_start'] = start[0]
            context['sec_start'] = start[1]
            context['min_end'] = end[0]
            context['sec_end'] = end[1]

            context['order_details'] = details
            if order_data.order_project_orderfilmmaking.filter(distribution__name='web/streaming').exists():
                web = order_data.order_dist_web.get(order=order_data.id)
                context['web'] = IndieWebDistribution(instance=web)
            if order_data.order_project_orderfilmmaking.filter(distribution__name='externally').exists():
                ext = order_data.order_dist_ext.get(order=order_data.id)
                context['ext'] = IndieExtDistribution(instance=ext)
        if order_data and order_data.project_type.name.lower() == 'programming':
            prog_data = order_data.order_project_orderprogramming.get(order=order_data.id)
            context['program_form'] = OrderProgramForm(instance=prog_data)
            details = order_data.order_details_orderprogrammingdetail.get(order=order_data.id)
            context['details_form'] = ProgramDetailForm(instance=details)
            context['order_details'] = details
            start = details.start_duration.split(':')
            end = details.end_duration.split(':')
            context['min_start'] = start[0]
            context['sec_start'] = start[1]
            context['min_end'] = end[0]
            context['sec_end'] = end[1]
            if order_data.order_project_orderprogramming.filter(distribution__name='web/streaming').exists():
                web = order_data.order_dist_web.get(order=order_data.id)
                context['web'] = IndieWebDistribution(instance=web)
            if order_data.order_project_orderprogramming.filter(distribution__name='externally').exists():
                ext = order_data.order_dist_ext.get(order=order_data.id)
                context['ext'] = IndieExtDistribution(instance=ext)
            if order_data.order_project_orderprogramming.filter(distribution__name='tv').exists():
                tv = order_data.order_tv_dist.get(order=order_data.id)
                context['tv'] = TvDistributionForm(instance=tv)
        elif order_data and order_data.project_type.name.lower() == 'advertising':
            ad_data = order_data.order_project_orderadvertising.get(order=order_data.id)
            context['advertising_form'] = OrderAdvertisingForm(instance=ad_data)
            details = order_data.order_details_orderadvertisingdetail.get(order=order_data.id)
            context['order_details'] = details
            start = details.start_duration.split(':')
            end = details.end_duration.split(':')
            context['min_start'] = start[0]
            context['sec_start'] = start[1]
            context['min_end'] = end[0]
            context['sec_end'] = end[1]
            context['details_form'] = AdvertisingDetailForm(instance=details)
            if order_data.order_project_orderadvertising.filter(distribution__name='web/streaming').exists():
                web = order_data.order_dist_web.get(order=order_data.id)
                context['web'] = IndieWebDistribution(instance=web)
            if order_data.order_project_orderadvertising.filter(distribution__name='externally'):
                ext = order_data.order_dist_ext.get(order=order_data.id)
                context['ext'] = IndieExtDistribution(instance=ext)
            # if order_data.order_project_orderadvertising.filter(distribution__name='tv').exists():
                # tv = order_data.order_tv_dist.get(order=order_data.id)
                # context['tv'] = TvDistributionForm(instance=tv)
        elif order_data and order_data.project_type.name.lower() == 'wedding':
            details = order_data.orderwedding_details.get(order=order_data.id)
            context['wedding_form'] = WeddingDetailForm(instance=details)
        elif order_data and order_data.project_type.name.lower() == 'personal use':
            details = order_data.orderpersonal_details.get(order=order_data.id)
            context['personal_form'] = PersonalDetailForm(instance=details)

        return context

    def get(self, request, order_id=None):
        context = self.data(request.user, order_id)
        return render(request,
                      'accounts/client-dash.html',
                      context=context)

    def post(self, request, order_id=None):
        # context = self.data(request.user, order_id)
        data = request.POST.copy()
        data['start_duration'] = request.POST['min_start'] + ':' + request.POST['sec_start']
        data['end_duration'] = request.POST['min_end'] + ':' + request.POST['sec_end']

        order_data = Order.objects.get(pk=order_id)
        order_form = OrderForm(request.POST)

        orders_list = Order.objects.filter(user=request.user).select_related()
        owners = OwnerDatabase.objects.all()

        ask_user = Question.objects.filter(order=order_data.id)

        context = {
            'url': 'client_dash',
            'orders_list': orders_list,
            'order_data': order_data,
            'order_form': order_form,
            'ask_user': ask_user,
            'owners': owners,
        }

        if order_data.project_type.name.lower() == 'film making':
            indie_form = OrderIndieForm(request.POST)
            indie_details_form = IndieDetailForm(data)
            context['indie_form'] = indie_form
            context['details_form'] = indie_details_form
            if order_data.order_project_orderfilmmaking.filter(distribution__name='web/streaming').exists():
                web = IndieWebDistribution(request.POST)
                context['web'] = web
                if web.is_valid():
                    web.save()
            if order_data.order_project_orderfilmmaking.filter(distribution__name='externally').exists():
                ext = IndieExtDistribution(request.POST)
                context['ext'] = ext
                if ext.is_valid():
                    ext.save()

            if indie_form.is_valid():
                indie_form.save()

            if indie_details_form.is_valid():
                details = indie_details_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.order_details_orderindieprojectdetail.get(order=order_data.id)

        if order_data.project_type.name.lower() == 'programming':
            program_form = OrderProgramForm(request.POST)
            context['program_form'] = program_form
            prog_details_form = ProgramDetailForm(data)
            context['details_form'] = prog_details_form

            if order_data.order_project_orderprogramming.filter(distribution__name='web/streaming').exists():
                web = IndieWebDistribution(request.POST)
                context['web'] = web
                if web.is_valid():
                    web.save()
            if order_data.order_project_orderprogramming.filter(distribution__name='externally').exists():
                ext = IndieExtDistribution(request.POST)
                context['ext'] = ext
                if ext.is_valid():
                    ext.save()
            if order_data.order_project_orderprogramming.filter(distribution__name='tv').exists():
                tv = TvDistributionForm(request.POST)
                context['tv'] = tv
                if tv.is_valid():
                    tv.save()

            if program_form.is_valid():
                program_form.save()
            if prog_details_form.is_valid():
                details = prog_details_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.order_details_orderprogrammingdetail.get(order=order_data.id)

        elif order_data and order_data.project_type.name.lower() == 'advertising':
            ad_form = OrderAdvertisingForm(request.POST)
            context['advertising_form'] = ad_form
            ad_details_form = AdvertisingDetailForm(data)
            context['details_form'] = ad_details_form

            if order_data.order_project_orderadvertising.filter(distribution__name='web/streaming').exists():
                web = IndieWebDistribution(request.POST)
                context['web'] = web
                if web.is_valid():
                    web.save()
            if order_data.order_project_orderadvertising.filter(distribution__name='externally'):
                ext = IndieExtDistribution(request.POST)
                context['ext'] = ext
                if ext.is_valid():
                    ext.save()
            if ad_form.is_valid():
                print('ad form is valid')
                ad_form.save()
            else:
                print(ad_form.errors)
            if ad_details_form.is_valid():
                details = ad_details_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.order_details_orderadvertisingdetail.get(order=order_data.id)
            # if order_data.order_project_orderadvertising.filter(distribution__name='tv').exists():
                # context['tv'] = TvDistributionForm(request.POST)

        elif order_data and order_data.project_type.name.lower() == 'wedding':
            wedding_form = WeddingDetailForm(request.POST)
            context['wedding_form'] = wedding_form
            if wedding_form.is_valid():
                details = wedding_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.orderwedding_details.get(order=order_data.id)

        elif order_data and order_data.project_type.name.lower() == 'personal use':
            personal_form = PersonalDetailForm(request.POST)
            context['personal_form'] = personal_form
            if personal_form.is_valid():
                details = personal_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.orderpersonal_details.get(order=order_data.id)
        else:
            print('what is going on??')
            print(order_data.project_type.name)

        if order_form.is_valid():
            order_form.save()

        return render(request, self.template_name, context)
