from django.db import IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login

from search.models import Track
from accounts.forms import PersonalInfoForm
from .models import *
from .forms import *


class OrderView(View):
    '''
    The order page
    '''
    def get(self, request, pk, *args, **kwargs):
        '''
        Return the order page
        :param request:
        :return:
        '''
        track = Track.objects.get(pk=pk)
        order_form = OrderForm(initial={
            'song_title': track.name,
            'performer_name': track.artist
        })
        return render(request,
                      'orders/order.html',
                      context={'form': order_form, 'pk': pk})

    def post(self, request, pk):
        form = OrderForm(request.POST)
        if form.is_valid():
            order_id = form.save()
            return HttpResponseRedirect(reverse(order_id.project_type.slug, args=[int(pk), order_id.id]))

        return render(request,
                      'orders/order.html',
                      context={'form': form, 'pk': pk})


class OrderIndieView(View):
    def get(self, request, pk, order_id):
        try:
            order = OrderFilmMaking.objects.filter(order=order_id)[0]
            form = OrderIndieForm(initial=order)
        except IndexError:
            form = OrderIndieForm()

        return render(request,
                      'orders/order_indie.html',
                      context={'form': form, 'pk': pk, 'order': order_id})

    def post(self, request, pk, order_id):
        form = OrderIndieForm(request.POST.copy())
        form.data['order'] = order_id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('indie_dist', args=[int(pk), order_id]))
        return render(request,
                      'orders/order_indie.html',
                      context={'form': form, 'pk': pk, 'order': order_id}
                      )


class OrderProgramView(View):
    def get(self, request, pk, order_id):
        try:
            order = OrderProgramming.objects.filter(order=order_id)[0]
            form = OrderProgramForm(initial=order)
        except IndexError:
            form = OrderProgramForm()

        return render(request,
                      'orders/order_program.html',
                      context={'form': form, 'pk': pk, 'order': order_id})

    def post(self, request, pk, order_id):
        form = OrderProgramForm(request.POST.copy())
        form.data['order'] = order_id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('prog_dist', args=[int(pk), order_id]))
        return render(request,
                      'orders/order_program.html',
                      context={'form': form, 'pk': pk, 'order': order_id}
                      )


class IndieDistribution(View):
    def get(self, request, pk, order_id):
        web_form = IndieWebDistribution()
        ext_form = IndieExtDistribution()

        order_dist = OrderFilmMaking.objects.filter(order=order_id)[0]

        context = {
            'pk': pk,
            'order': order_id,
            'url': 'distribution',
        }

        dist_list = [dist.__str__() for dist in order_dist.distribution.all()]

        if 'web/streaming' in dist_list:
            context['web'] = web_form
        if 'external' in dist_list:
            context['ext'] = ext_form

        context['form_url'] = 'indie_dist'

        return render(request,
                      'orders/indie_distribution.html',
                      context=context)

    def post(self, request, pk, order_id):
        web_form = None
        ext_form = None

        if 'distribute_on' in request.POST:
            web_form = IndieWebDistribution(request.POST.copy())
            web_form.data['order'] = order_id
        if 'name' in request.POST:
            ext_form = IndieExtDistribution(request.POST.copy())
            ext_form.data['order'] = order_id

        if web_form and not web_form.is_valid() or ext_form and not ext_form.is_valid():
            return render(request,
                          'orders/indie_distribution.html',
                          context={
                              'web': web_form,
                              'ext': ext_form,
                              'pk': pk,
                              'order': order_id,
                              'url': 'distribution',
                          })

        if web_form:
            web_form.save()
        if ext_form:
            ext_form.save()

        return HttpResponseRedirect(reverse('indie_details', args=[int(pk), order_id]))


class ProgramDistribution(View):
    def get(self, request, pk, order_id):
        web_form = IndieWebDistribution()
        ext_form = IndieExtDistribution()
        tv_form = TvDistributionForm()

        order_dist = OrderProgramming.objects.filter(order=order_id)[0]

        context = {
            'pk': pk,
            'order': order_id,
            'url': 'distribution',
        }

        dist_list = [dist.__str__() for dist in order_dist.distribution.all()]

        if 'web/streaming' in dist_list:
            context['web'] = web_form
        if 'external' in dist_list:
            context['ext'] = ext_form
        if 'tv' in dist_list:
            context['tv'] = tv_form

        context['form_url'] = 'prog_dist'

        return render(request,
                      'orders/program_distribution.html',
                      context=context)

    def post(self, request, pk, order_id):
        web_form = None
        ext_form = None
        tv_form = None

        if 'distribute_on' in request.POST:
            web_form = IndieWebDistribution(request.POST.copy())
            web_form.data['order'] = order_id
        if 'name' in request.POST:
            ext_form = IndieExtDistribution(request.POST.copy())
            ext_form.data['order'] = order_id
        if 'tv_trailer' or 'tv_program' in request.POST:
            tv_form = TvDistributionForm(request.POST.copy())
            tv_form.data['order'] = order_id

        if web_form and not web_form.is_valid() or ext_form and not ext_form.is_valid() or tv_form and not tv_form.is_valid():
            return render(request,
                          'orders/program_distribution.html',
                          context={
                              'web': web_form,
                              'ext': ext_form,
                              'tv': tv_form,
                              'pk': pk,
                              'order': order_id,
                              'url': 'distribution',
                          })

        if web_form:
            web_form.save()
        if ext_form:
            ext_form.save()
        if tv_form:
            print('in tv_form')
            tv_form.save()
        print('end of form')

        return HttpResponseRedirect(reverse('program_details', args=[int(pk), order_id]))


class IndieDetail(View):
    def get(self, request, pk, order_id):
        form = IndieDetailForm()
        personal_info = PersonalInfoForm()
        return render(request,
                      'orders/indie_detail.html',
                      context={
                          'form': form,
                          'personal_info': personal_info,
                          'pk': pk,
                          'order': order_id,
                          'url': 'details',
                      })

    def post(self, request, pk, order_id):
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        data = request.POST.copy()

        form = IndieDetailForm(request.POST)
        personal_info = PersonalInfoForm(request.POST.copy())

        if not password or not confirm_password:
            return render(request,
                          'orders/indie_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })

        if password != confirm_password:
            return render(request,
                          'orders/indie_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })

        data['order'] = order_id

        form = IndieDetailForm(data)
        if form.is_valid():
            form.save()
        else:
            return render(request,
                          'orders/indie_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })

        try:
            user = User.objects.create_user(username, email, password)
            print(user.id)
            login(request, user)
            data['user'] = user.id
            personal_info = PersonalInfoForm(data)
            if personal_info.is_valid():
                personal_info.save()
            else:
                return render(request,
                              'orders/indie_detail.html',
                              context={
                                  'form': form,
                                  'personal_info': personal_info,
                                  'pk': pk,
                                  'order': order_id,
                                  'url': 'details',
                                  'first_name': first_name,
                                  'last_name': last_name,
                                  'email': email,
                              })
            form.data['order'] = order_id
            print('hello')

            return HttpResponseRedirect(reverse('my_account'))

        except IntegrityError:
            return render(request,
                          'orders/indie_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })


class ProgramDetail(View):
    def get(self, request, pk, order_id):
        form = ProgramDetailForm()
        personal_info = PersonalInfoForm()

        return render(request,
                      'orders/indie_detail.html',
                      context={
                          'form': form,
                          'personal_info': personal_info,
                          'pk': pk,
                          'order': order_id,
                          'url': 'details',
                      })

    def post(self, request, pk, order_id):
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        data = request.POST.copy()

        form = ProgramDetailForm(request.POST)
        personal_info = PersonalInfoForm(request.POST.copy())

        if not password or not confirm_password:
            return render(request,
                          'orders/program_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })

        if password != confirm_password:
            return render(request,
                          'orders/program_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })

        data['order'] = order_id

        form = ProgramDetailForm(data)
        if form.is_valid():
            form.save()
        else:
            return render(request,
                          'orders/program_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })

        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            data['user'] = user.id
            personal_info = PersonalInfoForm(data)
            if personal_info.is_valid():
                personal_info.save()
            else:
                return render(request,
                              'orders/program_detail.html',
                              context={
                                  'form': form,
                                  'personal_info': personal_info,
                                  'pk': pk,
                                  'order': order_id,
                                  'url': 'details',
                                  'first_name': first_name,
                                  'last_name': last_name,
                                  'email': email,
                              })
            form.data['order'] = order_id

            return HttpResponseRedirect(reverse('my_account'))

        except IntegrityError:
            return render(request,
                          'orders/indie_detail.html',
                          context={
                              'form': form,
                              'personal_info': personal_info,
                              'pk': pk,
                              'order': order_id,
                              'url': 'details',
                              'first_name': first_name,
                              'last_name': last_name,
                              'email': email,
                          })
