import logging
import traceback
from datetime import timedelta

from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.utils import timezone

from orders.models import Order
from owners.models import Question, OrderOwnerRight, OwnerDatabase
from common.helpers import generate_password
from common.models import SiteFiles

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
        PersonalDetailForm,
    )
    from accounts.models import UserQuestion, AskUser, PersonalInfo, UserImage, ResetPassword, CounterOffer
    from accounts.forms import PersonalInfoForm, CounterOfferForm, UserQuestionForm
    from orders.models import (
    OrderFilmMaking,
    OrderProgramming,
    OrderAdvertising,
    OrderWedding,
    OrderPersonal,
    OrderDistributionIndie,
    OrderDistributionProgramming,
    ExternalDistribution,
    WebDistribution,
    TvDistribution,
    OrderIndieProjectDetail,
    OrderProgrammingDetail,
    OrderAdvertisingDetail
    )


class ConnectBase(View):
    '''
    base class for login and signup classes
    '''
    def add_order_user(self, request, user):
        '''
        adding the order to the newly connected user
        :param request: the request object
        :param user: the user object
        :return:
        '''
        if 'order_user' in request.session.keys():
            order = Order.objects.get(pk=request.session['order_id'])
            order.user = user
            order.save()
            del request.session['order_user']
            del request.session['order_id']
            return order.id


class LoginView(ConnectBase):
    '''
    login cloass to handle http methods for login
    '''
    def get(self, request):
        '''
        showing the login page with a bit of logic.

        if we have an order id in the session it means the user did an order and we
        didn't handle it yet, so we handle what needs to
        :param request: the request object
        :return: the login page
        '''
        if 'order_id' in request.session:
            order_id = request.session['order_id']
            detail_forms = [
                request.build_absolute_uri(reverse('indie_details', args={order_id})),
                request.build_absolute_uri(reverse('program_details', args={order_id})),
                request.build_absolute_uri(reverse('advertising_details', args={order_id})),
                request.build_absolute_uri(reverse('personal_use', args={order_id})),
                request.build_absolute_uri(reverse('wedding', args={order_id})),
            ]

            if 'HTTP_REFERER' in request.META and request.META['HTTP_REFERER'] in detail_forms:
                request.session['order_user'] = True

        return render(request,
                      'accounts/login.html',
                      context={'is_form': True})

    def post(self, request):
        '''
        check if the user is registered and act accordingly
        :param request: the request object
        :return: redirect to the appropriate page
        '''
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            order = self.add_order_user(request, user)
            if order:
                send_mail('licenseit- thanks for ordering',
                          'thanks for ordering, here is a link for your order {0}'
                          .format(request.META['HTTP_HOST'] + reverse('my_account_order',
                                                                      args=[order])),
                      'support@licenseit.net',
                      [user.email],
                      html_message='')
            return HttpResponseRedirect(reverse('my_account'))
        else:
            return render(request,
                          'accounts/login.html',
                          context={
                              'error': 'username or password is wrong',
                              'is_form': True
                          })


class SignupView(ConnectBase):
    '''
    handling the signup
    '''
    def post(self, request):
        '''
        signup the user
        :param request: the request object
        :return: redirect to the appropriate page
        '''
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password']
        # first_name = request.POST['first']
        # last_name = request.POST['last']
        confirm = request.POST['confirm']

        if password != confirm:
            return render(request,
                          'home/index.html',
                          context={'error': 'this email is already registered'})

        try:
            user = User.objects.create_user(username, email, password)
            # user.first_name = first_name
            # user.last_name = last_name
            # user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            self.add_order_user(request, user)
        except IntegrityError:
            return render(request,
                          'home/index.html',
                          context={'error': 'this email is already registered'})
        send_mail('licenseit- thanks for registering',
                  'Thanks for registering to our site',
                  'cdo@licenseit.net',
                  [email],
                  html_message='<h3>hello</h3>')
        return HttpResponseRedirect(reverse('search'))


class ForgotPassword(View):
    def post(self, request):
        '''
        handling the data when wanting to reset the password
        :param request: the request object
        :return: redirecting the user to the home page
        '''
        user = User.objects.get(email=request.POST['email'])
        if not user:
            return render(request,
                          'home/index.html',
                          context={'error_forgot_password': "we don't have this user on the system"})
        reset_token = generate_password(50)
        reset_pass = ResetPassword()
        reset_pass.reset_token = reset_token
        reset_pass.user = user
        reset_pass.save()
        send_mail('licenseit reset password',
                  'reset your password via this link: {0}/accounts/{1}/'.format(request.get_host(), reset_token),
                  'cdo@licenseit.net',
                  [user.email])
        return render(request, 'home/index.html')


class ChangePassword(View):
    '''
    handling changing password
    '''
    def is_valid(self, string=None):
        '''
        checking if the link was entered within allowed time and resetting password
        :param string: the reset token
        :return: boolean, True if valid, False otherwise
        '''
        if not string:
            return False
        try:
            reset_pass = ResetPassword.objects.get(reset_token=string)
        except ResetPassword.DoesNotExist:
            return False
        now = timezone.now()
        margin = timedelta(1)
        if now - margin < reset_pass.created:
            return True
        return False

    def get(self, request, string=None):
        '''
        the page for changing password on reset password
        :param request: request object
        :param string: the reset token
        :return: reset password if string is valid, home page otherwise
        '''
        if self.is_valid(string):
            return render(request,
                          'accounts/reset_password.html',
                          context={'string': string})
        return HttpResponseRedirect(reverse('home'))

    def post(self, request, string=None):
        '''
        actually changing the password if all is valid
        :param request: request object
        :param string: reset token
        :return: redirect to home if all is well, if not staying on the page with error massage
        '''
        if self.is_valid(string) and 'password' in request.POST and 'confirm_pass' in request.POST:
            if request.POST['password'] == request.POST['confirm_pass']:
                reset_pass = ResetPassword.objects.get(reset_token=string)
                user = reset_pass.user
                user.set_password(request.POST['password'])
                user.save()
                return HttpResponseRedirect(reverse('home'))
            return render(request,
                          'accounts/reset_password.html',
                          context={
                              'error': 'password and confirm password were not identical',
                              'string': string
                          })
        return HttpResponseRedirect(reverse('home'))


class EditUserData(View):
    '''
    edit user data on the client dash page
    '''
    def post(self, request):
        '''
        edit the user data according to the data we receive
        :param request: request object
        :return: the page of my account
        '''
        data = request.POST.copy()

        user = User.objects.get(username=request.user.username)
        data['user'] = user.id
        personal_info = PersonalInfoForm(data)

        if 'first_name' in request.POST and request.POST['first_name']:
            user.first_name = request.POST['first_name']
            user.save()
        if 'last_name' in request.POST and request.POST['last_name']:
            user.last_name = request.POST['last_name']
            user.save()
        if 'email' in request.POST and request.POST['email']:
            user.email = request.POST['email']
            user.save()
        if 'password' in request.POST and 'confirm_password' in request.POST and request.POST['password']:
            pas = request.POST['password']
            pas2 = request.POST['confirm_password']
            if pas == pas2:
                user.password = pas
                user.save()

        if personal_info.is_valid():
            personal_info.save()

        return HttpResponseRedirect(reverse('my_account'))


class Account(ConnectBase):
    '''
    client dash page
    '''
    template_name = 'accounts/client-dash.html'

    def data(self, user, order_id=None):
        '''
        getting all the data for the client dash page
        :param user:
        :param order_id:
        :return:
        '''
        orders_list = Order.objects.filter(user=user).filter(is_done=True).select_related()

        if order_id:
            order_data = Order.objects.get(pk=order_id)
        elif orders_list:
            order_data = orders_list.last()
        else:
            order_data = False

        if order_data:
            owners = OrderOwnerRight.objects.filter(order=order_data.id)
            ask_user = Question.objects.filter(order=order_data.id)
        else:
            ask_user = ''
            owners = ''

        if PersonalInfo.objects.filter(user=user).exists():
            personal_info = PersonalInfo.objects.get(user=user)
            personal_info_form = PersonalInfoForm(instance=personal_info)
        else:
            personal_info_form = PersonalInfoForm()

        user_data = User.objects.get(username=user.username)

        if order_data and CounterOffer.objects.filter(order=order_data.id).exists():
            counter_offer = CounterOffer.objects.filter(order=order_data.id)[0]
            counter = CounterOfferForm(instance=counter_offer)
        else:
            counter = CounterOfferForm()

        if order_data:
            order_form = OrderForm(instance=order_data)
        else:
            order_form = OrderForm()

        context = {
            'url': 'client_dash',
            'orders_list': orders_list,
            'order_data': order_data,
            'order_form': order_form,
            'ask_user': ask_user,
            'owners': owners,
            'is_form': True,
            'personal_info': personal_info_form,
            'user_data': UserChangeForm(instance=user_data),
            'user': user,
            'counter_offer_form': counter
        }

        # check the type of the project, since it affects the model we need to work with
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

            context['film_making'] = OrderFilmMaking.objects.get(order=order_data.id)
            context['details'] = OrderIndieProjectDetail.objects.get(order=order_data.id)

            context['order_details'] = details
            # check which type of distribution and act accordingly
            if order_data.order_project_orderfilmmaking.filter(distribution__name__iexact='web/streaming').exists():
                web = order_data.order_dist_web.get(order=order_data.id)
                context['web'] = IndieWebDistribution(instance=web)
                context['web_dist'] = web
            if order_data.order_project_orderfilmmaking.filter(distribution__name__iexact='externally').exists():
                ext = order_data.order_dist_ext.get(order=order_data.id)
                context['ext'] = IndieExtDistribution(instance=ext)
                context['ext_dist'] = ext

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

            context['programming'] = OrderProgramming.objects.get(order=order_data.id)
            context['details'] = OrderProgrammingDetail.objects.get(order=order_data.id)

            # check which type of distribution and act accordingly
            if order_data.order_project_orderprogramming.filter(distribution__name='web/streaming').exists():
                web = order_data.order_dist_web.get(order=order_data.id)
                context['web'] = IndieWebDistribution(instance=web)
                context['web_dist'] = web
            if order_data.order_project_orderprogramming.filter(distribution__name='externally').exists():
                ext = order_data.order_dist_ext.get(order=order_data.id)
                context['ext'] = IndieExtDistribution(instance=ext)
                context['ext_dist'] = ext
            if order_data.order_project_orderprogramming.filter(distribution__name='tv').exists():
                tv = order_data.order_tv_dist.get(order=order_data.id)
                context['tv'] = TvDistributionForm(instance=tv)
                context['tv_dist'] = tv
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

            context['advertising'] = OrderAdvertising.objects.get(order=order_data.id)
            context['details'] = OrderAdvertisingDetail.objects.get(order=order_data.id)

            context['details_form'] = AdvertisingDetailForm(instance=details)

            # check which type of distribution and act accordingly
            if order_data.order_project_orderadvertising.filter(distribution__name='web/streaming').exists():
                web = order_data.order_dist_web.get(order=order_data.id)
                context['web'] = IndieWebDistribution(instance=web)
                context['web_dist'] = web
            if order_data.order_project_orderadvertising.filter(distribution__name='externally'):
                ext = order_data.order_dist_ext.get(order=order_data.id)
                context['ext'] = IndieExtDistribution(instance=ext)
                context['ext_dist'] = ext
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

    def get(self, request, order_id=None, payment_id=None):
        '''
        the page of client dash
        :param request: request object
        :param order_id: the order id
        :return: client dash page
        '''
        self.add_order_user(request, request.user)
        context = self.data(request.user, order_id)
        context['user_question_form'] = UserQuestionForm()
        order = context['order_data']
        if order:
            context['user_question_history'] = UserQuestion.objects.filter(order=order.id)
            context['owner_questions'] = Question.objects.filter(order=order.id).select_related()
            context['counter_owners'] = CounterOffer.objects.filter(order=order.id)

        if payment_id:
            context['payment_id'] = payment_id
        image = SiteFiles.objects.filter(file_name='default_image')
        if image:
            context['image'] = image[0].file.url

        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request, order_id=None):
        '''
        process the data and save if all is well.
        :param request: request object
        :param order_id: order id
        :return: client dash page
        '''
        order_data = Order.objects.get(pk=order_id)

        data = request.POST.copy()
        if 'personal_use' != order_data.project_type.slug != 'wedding':
            data['start_duration'] = request.POST['min_start'] + ':' + request.POST['sec_start']
            data['end_duration'] = request.POST['min_end'] + ':' + request.POST['sec_end']

        order_form = OrderForm(request.POST, instance=order_data)

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
            'is_form': True,
        }

        # we need to check the project type to be able to work with the right model
        if order_data.project_type.name.lower() == 'film making':
            order_film = OrderFilmMaking.objects.get(order=order_data.id)
            indie_form = OrderIndieForm(request.POST, instance=order_film)
            indie_details = OrderIndieProjectDetail.objects.get(order=order_data.id)
            indie_details_form = IndieDetailForm(data, instance=indie_details)
            context['indie_form'] = indie_form
            context['details_form'] = indie_details_form
            # need to check which distribution was selected to make sure on the right model
            web_distribution = order_data.order_project_orderfilmmaking.filter(distribution__name='web/streaming')
            if web_distribution.exists():
                web = IndieWebDistribution(request.POST, instance=web_distribution.first())
                context['web'] = web
                if web.is_valid():
                    web.save()
            ext_distribution = order_data.order_project_orderfilmmaking.filter(distribution__name='externally')
            if ext_distribution.exists():
                ext = IndieExtDistribution(request.POST, instance=ext_distribution.first())
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
            program = OrderProgramming.objects.get(order=order_data.id)
            program_form = OrderProgramForm(request.POST, instance=program)
            context['program_form'] = program_form
            prog_details = OrderProgrammingDetail.objects.get(order=order_data.id)
            prog_details_form = ProgramDetailForm(data, instance=prog_details)
            context['details_form'] = prog_details_form

            # need to check which distribution was selected to make sure on the right model
            web_dist = order_data.order_project_orderprogramming.filter(distribution__name='web/streaming')
            if web_dist.exists():
                web = IndieWebDistribution(request.POST, instance=web_dist.first())
                context['web'] = web
                if web.is_valid():
                    web.save()
            ext_dist = order_data.order_project_orderprogramming.filter(distribution__name='externally')
            if ext_dist.exists():
                ext = IndieExtDistribution(request.POST, instance=ext_dist.first())
                context['ext'] = ext
                if ext.is_valid():
                    ext.save()
            tv_dist = order_data.order_project_orderprogramming.filter(distribution__name='tv')
            if tv_dist.exists():
                tv = TvDistributionForm(request.POST, tv_dist.first())
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
            ads = OrderAdvertising.objects.get(order=order_data.id)
            ad_form = OrderAdvertisingForm(request.POST, instance=ads)
            context['advertising_form'] = ad_form
            ad_details = OrderAdvertisingDetail.objects.get(order=order_data.id)
            ad_details_form = AdvertisingDetailForm(data, instance=ad_details)
            context['details_form'] = ad_details_form

            # need to check which distribution was selected to make sure on the right model
            web_distrib = order_data.order_project_orderadvertising.filter(distribution__name='web/streaming')
            if web_distrib.exists():
                web = IndieWebDistribution(request.POST, instance=web_distrib.first())
                context['web'] = web
                if web.is_valid():
                    web.save()
            ext_distrib = order_data.order_project_orderadvertising.filter(distribution__name='externally')
            if ext_distrib.exists():
                ext = IndieExtDistribution(request.POST, instance=ext_distrib.first())
                context['ext'] = ext
                if ext.is_valid():
                    ext.save()

            if ad_form.is_valid():
                ad_form.save()

            if ad_details_form.is_valid():
                details = ad_details_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.order_details_orderadvertisingdetail.get(order=order_data.id)
            # if order_data.order_project_orderadvertising.filter(distribution__name='tv').exists():
                # context['tv'] = TvDistributionForm(request.POST)

        elif order_data and order_data.project_type.name.lower() == 'wedding':
            wedding = OrderWedding.objects.get(order=order_data.id)
            wedding_form = WeddingDetailForm(request.POST, instance=wedding)
            context['wedding_form'] = wedding_form
            if wedding_form.is_valid():
                details = wedding_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.orderwedding_details.get(order=order_data.id)

        elif order_data and order_data.project_type.name.lower() == 'personal use':
            personal = OrderPersonal.objects.get(order=order_data.id)
            personal_form = PersonalDetailForm(request.POST, instance=personal)
            context['personal_form'] = personal_form
            if personal_form.is_valid():
                details = personal_form.save()
                context['order_details'] = details
            else:
                context['order_details'] = order_data.orderpersonal_details.get(order=order_data.id)

        if order_form.is_valid():
            order_form.save()

        return render(request, self.template_name, context)


class CounterOfferView(View):
    '''
    counter offer logic
    '''
    def post(self, request, order_id=None):
        '''
        here we are going to handle the counter offer data after submitting on client dash
        :param request: request object
        :param order_id: order id
        :return: client dash page
        '''
        owner = OwnerDatabase.objects.get(name=request.POST['owner'])
        if order_id:
            counter_offer = CounterOffer.objects.filter(owner=owner.id).filter(order=order_id).first()
        else:
            order_id = Order.objects.filter(user=request.user).first().id
            counter_offer = CounterOffer.objects.filter(owner=owner.id).filter(order=order_id).first()
        data = request.POST.copy()
        data['owner'] = owner.id
        form = CounterOfferForm(data, instance=counter_offer)

        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('my_account_order', args={order_id}))


class UserQuestionView(View):
    def post(self, request, order_id):
        form = UserQuestionForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('my_account_order', args={order_id}))


class AskUserView(View):
    def post(self, request, order_id):
        for question, answer in request.POST.items():
            if question == 'csrfmiddlewaretoken':
                continue
            question = question.split('ion')[1]
            ask = Question.objects.get(pk=question)
            ask.answer = answer
            ask.save()
        return HttpResponseRedirect(reverse('my_account_order', args={order_id}))
