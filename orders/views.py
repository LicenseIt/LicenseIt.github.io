from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin

from search.models import Track
from accounts.forms import PersonalInfoForm
from .models import *

from owners.models import OrderOwnerRight, OwnerDatabase

import sys
if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
    from .forms import *


class OrderView(View):
    '''
    The order page
    '''
    template_name = 'orders/order.html'

    def get(self, request, song_id=None, *args, **kwargs):
        '''
        get the order page
        :param request: the request object
        :param song_id: the song id if available in our database
        :return:
        '''
        song_name = ''
        artist = ''
        if request.resolver_match.url_name == 'order':
            track = Track.objects.get(pk=song_id)
            song_name = track.name
            artist = track.artist
            order_form = OrderForm(initial={
                'song_title': song_name,
                'performer_name': artist
            })
        # we want a manual song title and performer name- url name is manual_order
        else:
            order_form = ManualOrderForm()

        return render(request,
                      self.template_name,
                      context={
                          'order_form': order_form,
                          'song_id': song_id,
                          'song_title': song_name,
                          'artist': artist,
                          'is_form': True,
                      })

    def post(self, request, song_id=None):
        '''
        processing the order
        :param request: the request object
        :param song_id: the song id
        :return:
        '''
        if request.resolver_match.url_name == 'order':
            form = OrderForm(request.POST.copy())
            form.data['song'] = song_id
        else:
            form = ManualOrderForm(request.POST)

        if form.is_valid():
            order_id = form.save()
            order_owner = OrderOwnerRight()
            if order_id.song:
                owner = OwnerDatabase.objects.filter(name=order_id.song.media_copyright)

                if owner:
                    order_owner.owner = owner
                    order_owner.order = order_id
                    order_owner.save()

            if request.user.is_authenticated():
                order_id.user = request.user
                order_id.save()

            return HttpResponseRedirect(reverse(order_id.project_type.slug, args=[order_id.id]))

        return render(request,
                      self.template_name,
                      context={
                          'order_form': form,
                          'song_id': song_id,
                          'is_form': True
                      })


class OrderIndieView(View):
    '''
    the film making page after choosing film making
    '''
    template_name = 'orders/order_indie.html'

    def get(self, request, order_id):
        '''
        get the film making page
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        try:
            order = OrderFilmMaking.objects.filter(order=order_id)[0]
            form = OrderIndieForm(initial=order)
        except IndexError:
            form = OrderIndieForm()
        except TypeError:
            form = OrderIndieForm()

        return render(request,
                      self.template_name,
                      context={'indie_form': form, 'order': order_id, 'is_form': True})

    def post(self, request, order_id):
        '''
        processing the film making data and continue to the right page afterwards
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = OrderIndieForm(request.POST.copy())
        form.data['order'] = order_id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('indie_dist', args=[order_id]))
        return render(request,
                      self.template_name,
                      context={'indie_form': form, 'order': order_id, 'is_form': True}
                      )


class OrderProgramView(View):
    '''
    the programming page after choosing programming
    '''
    template_name = 'orders/order_program.html'

    def get(self, request, order_id):
        '''
        get the programming page
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        try:
            order = OrderProgramming.objects.filter(order=order_id)[0]
            form = OrderProgramForm(initial=order)
        except IndexError:
            form = OrderProgramForm()

        return render(request,
                      self.template_name,
                      context={'program_form': form, 'order': order_id, 'is_form': True})

    def post(self, request, order_id):
        '''
        processing the data from the programming page
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = OrderProgramForm(request.POST.copy())
        form.data['order'] = order_id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('prog_dist', args=[order_id]))
        return render(request,
                      self.template_name,
                      context={'program_form': form, 'order': order_id, 'is_form': True}
                      )


class OrderAdvertisingView(View):
    '''
    the advertising view
    '''
    template_name = 'orders/order_Advertising.html'

    def get(self, request, order_id):
        '''
        get the advertising form page
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        try:
            order = OrderAdvertising.objects.filter(order=order_id)[0]
            form = OrderAdvertisingForm(initial=order)
        except IndexError:
            form = OrderAdvertisingForm()

        return render(request,
                      self.template_name,
                      context={'advertising_form': form, 'order': order_id, 'is_form': True})

    def post(self, request, order_id):
        '''
        processing the advertising data from the form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = OrderAdvertisingForm(request.POST.copy())
        form.data['order'] = order_id
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ad_dist', args=[order_id]))
        return render(request,
                      self.template_name,
                      context={'advertising_form': form, 'order': order_id, 'is_form': True}
                      )


class IndieDistribution(View):
    '''
    film making distribution form
    '''
    template_name = 'orders/indie_distribution.html'

    def get(self, request, order_id):
        '''
        get the film making distribution form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        web_form = IndieWebDistribution()
        ext_form = IndieExtDistribution()

        order_dist = OrderFilmMaking.objects.filter(order=order_id)[0]

        context = {
            'order': order_id,
            'url': 'distribution',
            'is_form': True,
        }

        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]
        print(dist_list)

        if 'web/streaming' in dist_list:
            context['web'] = web_form
        if 'externally' in dist_list:
            context['ext'] = ext_form

        if 'web' in context or 'ext' in context.keys():
            return render(request,
                          self.template_name,
                          context=context)
        else:
            return HttpResponseRedirect(reverse('indie_details', args=[order_id]))

    def post(self, request, order_id):
        '''
        processing the data from the film making distribution form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
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
                          self.template_name,
                          context={
                              'web': web_form,
                              'ext': ext_form,
                              'order': order_id,
                              'url': 'distribution',
                              'is_form': True
                          })

        if web_form:
            done = web_form.save()
            if web_form.data['distribute_new']:
                new_dist = WebEntry(name=web_form.data['distribute_new'])
                new_dist.full_clean()
                new_dist.save()
                dist = WebDistribution.objects.get(pk=done.id)
                dist.distribute_on.add(new_dist.id)
                dist.save()

        if ext_form:
            done = ext_form.save()
            if ext_form.data['dist_new']:
                new_dist = ExternalEntry(name=ext_form.data['dist_new'])
                new_dist.full_clean()
                new_dist.save()
                dist = ExternalDistribution.objects.get(pk=done.id)
                dist.distribute_on.add(new_dist.id)
                dist.save()

        return HttpResponseRedirect(reverse('indie_details', args=[order_id]))


class ProgramDistribution(View):
    '''
    the programming distribution form view
    '''
    template_name = 'orders/program_distribution.html'

    def get(self, request, order_id):
        '''
        get the programming distribution form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        web_form = IndieWebDistribution()
        ext_form = IndieExtDistribution()
        tv_form = TvDistributionForm()

        order_dist = OrderProgramming.objects.filter(order=order_id)[0]

        context = {
            'order': order_id,
            'url': 'distribution',
            'is_form': True,
        }

        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]

        if 'web/streaming' in dist_list:
            context['web'] = web_form
        if 'externally' in dist_list:
            context['ext'] = ext_form
        if 'tv' in dist_list:
            context['tv'] = tv_form

        if 'web' in context or 'ext' in context or 'tv' in context:
            return render(request,
                          self.template_name,
                          context=context)
        else:
            return HttpResponseRedirect(reverse('program_details', args=[order_id]))

    def post(self, request, order_id):
        '''
        processing the form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
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
                          self.template_name,
                          context={
                              'web': web_form,
                              'ext': ext_form,
                              'tv': tv_form,
                              'order': order_id,
                              'url': 'distribution',
                              'is_form': True,
                          })

        if web_form:
            done = web_form.save()
            if web_form.data['distribute_new']:
                new_dist = WebEntry(name=web_form.data['distribute_new'])
                new_dist.full_clean()
                new_dist.save()
                dist = WebDistribution.objects.get(pk=done.id)
                dist.distribute_on.add(new_dist.id)
                dist.save()

        if ext_form:
            done = ext_form.save()
            if ext_form.data['dist_new']:
                new_dist = ExternalEntry(name=ext_form.data['dist_new'])
                new_dist.full_clean()
                new_dist.save()
                dist = ExternalDistribution.objects.get(pk=done.id)
                dist.name.add(new_dist.id)
                dist.save()

        if tv_form:
            tv_form.save()

        return HttpResponseRedirect(reverse('program_details', args=[order_id]))


class AdvertisingDistribution(View):
    '''
    advertising distribution form
    '''
    template_name = 'orders/advertising_distribution.html'

    def get(self, request, order_id):
        '''
        get the advertising distribution form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        web_form = IndieWebDistribution()
        ext_form = IndieExtDistribution()
        # tv_form = TvDistributionForm()

        order_dist = OrderAdvertising.objects.filter(order=order_id)[0]

        context = {
            'order': order_id,
            'url': 'distribution',
            'is_form': True,
        }

        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]

        if 'web/streaming' in dist_list:
            context['web'] = web_form
        if 'external' in dist_list:
            context['ext'] = ext_form
        # if 'tv' in dist_list:
        #     context['tv'] = tv_form

        if 'web' in context or 'ext' in context: # or 'tv' in context:
            return render(request,
                          self.template_name,
                          context=context)
        else:
            return HttpResponseRedirect(reverse('advertising_details', args=[order_id]))

    def post(self, request, order_id):
        '''
        processing the data from advertising distribution form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        web_form = None
        ext_form = None
        # tv_form = None

        if 'distribute_on' in request.POST:
            web_form = IndieWebDistribution(request.POST.copy())
            web_form.data['order'] = order_id
        if 'name' in request.POST:
            ext_form = IndieExtDistribution(request.POST.copy())
            ext_form.data['order'] = order_id
        # if 'tv_trailer' or 'tv_program' in request.POST:
        #     tv_form = TvDistributionForm(request.POST.copy())
        #     tv_form.data['order'] = order_id

        if web_form and not web_form.is_valid() or ext_form and not ext_form.is_valid(): # or tv_form and not tv_form.is_valid():
            return render(request,
                          self.template_name,
                          context={
                              'web': web_form,
                              'ext': ext_form,
                              # 'tv': tv_form,
                              'order': order_id,
                              'url': 'distribution',
                              'is_form': True,
                          })

        if web_form:
            done = web_form.save()
            if web_form.data['distribute_new']:
                new_dist = WebEntry(name=web_form.data['distribute_new'])
                new_dist.full_clean()
                new_dist.save()
                dist = WebDistribution.objects.get(pk=done.id)
                dist.distribute_on.add(new_dist.id)
                dist.save()

        if ext_form:
            done = ext_form.save()
            if ext_form.data['dist_new']:
                new_dist = ExternalEntry(name=ext_form.data['dist_new'])
                new_dist.full_clean()
                new_dist.save()
                dist = ExternalDistribution.objects.get(pk=done.id)
                dist.distribute_on.add(new_dist.id)
                dist.save()

        # if tv_form:
        #     tv_form.save()

        return HttpResponseRedirect(reverse('advertising_details', args=[order_id]))


class DetailBase(View):
    def func(self, request, order_id, detail_form):
        data = request.POST.copy()
        data['order'] = order_id
        form = detail_form(data)

        context = {
            'details_form': form,
            'order': order_id,
            'url': 'details',
            'is_form': True,
        }

        not_valid = False

        if 'min_start' in data:
            context['min_start'] = request.POST['min_start']
        else:
            not_valid = True

        if 'sec_start' in data:
            context['sec_start'] = request.POST['sec_start']
        else:
            not_valid = True

        if 'min_end' in data:
            context['min_end'] = request.POST['min_end']
        else:
            not_valid = True

        if 'sec_end' in data:
            context['sec_end'] = request.POST['sec_end']
        else:
            not_valid = True

        if not_valid:
            return render(request, self.template_name, context=context)

        data['start_duration'] = request.POST['min_start'] + ':' + request.POST['sec_start']
        data['end_duration'] = request.POST['min_end'] + ':' + request.POST['sec_end']

        if 'rate' in request.POST:
            form_rate = RateUsForm(request.POST.copy())
            form_rate.data['order'] = order_id
            context['rate_form'] = form_rate
            if form_rate.is_valid():
                form_rate.save()

        if not request.user.is_authenticated():
            email = request.POST['email']
            username = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email
            personal_info = PersonalInfoForm(data)
            context['personal_info'] = personal_info

            if not password or not confirm_password or password != confirm_password:
                return render(request,
                              self.template_name,
                              context=context)

            try:
                user = User.objects.create_user(username, email, password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                data['user'] = user.id
                personal_info = PersonalInfoForm(data)
                context['personal_info'] = personal_info

                if personal_info.is_valid():
                    personal_info.save()
                else:
                    return render(request,
                                  self.template_name,
                                  context=context)

            except IntegrityError:
                context['error_user'] = 'there is already a user with this email'
                return render(request,
                              self.template_name,
                              context=context)

        if form.is_valid():
            form.save()
        else:
            return render(request,
                          self.template_name,
                          context=context)

        order = Order.objects.get(pk=order_id)
        if request.user.is_authenticated() and not order.user:
            order.user = request.user
        elif not order.user:
            order.user = data['user']
        order.save()

        if 'rate' in request.POST:
            return HttpResponseRedirect(reverse('my_account'))
        else:
            return HttpResponseRedirect(reverse('rate_us', args=[order_id]))


class IndieDetail(DetailBase):
    '''
    the details form view for film making
    '''
    template_name = 'orders/details.html'

    def get(self, request, order_id):
        '''
        get the film making details form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = IndieDetailForm()
        context = {
            'details_form': form,
            'order': order_id,
            'url': 'details',
            'is_form': True
        }
        if not request.user.is_authenticated():
            context['personal_info'] = PersonalInfoForm()

        order_dist = OrderFilmMaking.objects.filter(order=order_id)[0]
        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]

        if 'web/streaming' in dist_list or 'external' in dist_list:
            context['rate_form'] = RateUsForm()
            context['page_num'] = 4
        else:
            context['page_num'] = 3

        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request, order_id):
        '''
        processing the form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        return self.func(request, order_id, IndieDetailForm)


class ProgramDetail(DetailBase):
    '''
    programming details view
    '''
    template_name = 'orders/details.html'

    def get(self, request, order_id):
        '''
        get the programming details view
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = ProgramDetailForm()
        personal_info = PersonalInfoForm()

        order_dist = OrderProgramming.objects.filter(order=order_id)[0]
        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]

        context = {
            'details_form': form,
            'personal_info': personal_info,
            'order': order_id,
            'url': 'details',
            'is_form': True,
        }

        if 'web/streaming' in dist_list or 'external' in dist_list or 'tv' in dist_list:
            context['rate_form'] = RateUsForm()
            context['page_num'] = 4
        else:
            context['page_num'] = 3

        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request, order_id):
        '''
        processing the data from the form and logging in the user
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        return self.func(request, order_id, ProgramDetailForm)


class AdvertisingDetail(DetailBase):
    '''
    advertising details form view
    '''
    template_name = 'orders/details.html'

    def get(self, request, order_id):
        '''
        get the advertising detail form
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = AdvertisingDetailForm()
        personal_info = PersonalInfoForm()

        context = {
            'details_form': form,
            'personal_info': personal_info,
            'order': order_id,
            'url': 'details',
            'is_form': True,
        }

        order_dist = OrderAdvertising.objects.filter(order=order_id)[0]
        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]

        if 'web/streaming' in dist_list or 'external' in dist_list:
            context['rate_form'] = RateUsForm()
            context['page_num'] = 4
        else:
            context['page_num'] = 3

        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request, order_id):
        '''
        processing the form and logging in the user
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        return self.func(request, order_id, AdvertisingDetailForm)


class RateUsView(View):
    '''
    the view for a rate us page if we have only 3 forms on indie, programming or advertising
    '''

    def get(self, request, order_id):
        rate_form = RateUsForm()
        return render(request,
                      'orders/rate_us_form.html',
                      context={'rate_form': rate_form, 'order': order_id, 'is_form': True})

    def post(self, request, order_id):
        rate_form = RateUsForm(request.POST.copy())
        rate_form.data['order'] = order_id

        if rate_form.is_valid():
            rate_form.save()
            return HttpResponseRedirect(reverse('my_account'))
        return render(request,
                      'orders/rate_us_form.html',
                      context={'rate_form': rate_form, 'order': order_id, 'is_form': True})


class WeddingDetails(View):
    '''
    the wedding details form view
    '''
    template_name = 'orders/wedding_detail.html'

    def get(self, request, order_id):
        '''
        get the page
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = WeddingDetailForm()
        personal_info = PersonalInfoForm()

        return render(request,
                      self.template_name,
                      context={
                          'wedding_form': form,
                          'personal_info': personal_info,
                          'order': order_id,
                          'url': 'details',
                          'is_form': True,
                      })

    def post(self, request, order_id):
        '''
        processing the form and logging in the user
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        data = request.POST.copy()
        data['order'] = order_id

        form = WeddingDetailForm(data)
        context = {
            'wedding_form': form,
            'order': order_id,
            'url': 'details',
            'is_form': True,
        }

        if not request.user.is_authenticated():
            email = request.POST['email']
            context['email'] = email
            username = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            first_name = request.POST['first_name']
            context['first_name'] = first_name
            last_name = request.POST['last_name']
            context['last_name'] = last_name

            personal_info = PersonalInfoForm(request.POST.copy())
            context['personal_info'] = personal_info

            if not password or not confirm_password:
                return render(request,
                              self.template_name,
                              context=context)

            if password != confirm_password:
                return render(request,
                              self.template_name,
                              context=context)

            try:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                data['user'] = user.id
                personal_info.data['user'] = user

                if personal_info.is_valid():
                    personal_info.save()

                order = Order.objects.get(pk=order_id)
                order.user = user
                order.save()

            except IntegrityError:
                return render(request,
                              self.template_name,
                              context=context)

        if form.is_valid():
            form.save()
        else:
            return render(request,
                          self.template_name,
                          context=context)

        return HttpResponseRedirect(reverse('my_account'))


class PersonalDetails(View):
    '''
    the personal details form view
    '''
    template_name = 'orders/personal_detail.html'

    def get(self, request, order_id):
        '''
        get the page
        :param request: request object
        :param order_id: order id
        :return:
        '''
        form = PersonalDetailForm()
        personal_info = PersonalInfoForm()

        return render(request,
                      self.template_name,
                      context={
                          'personal_form': form,
                          'personal_info': personal_info,
                          'order': order_id,
                          'url': 'details',
                          'is_form': True,
                      })

    def post(self, request, order_id):
        '''
        processing the form and logging in the user
        :param request: request object
        :param order_id: order id
        :return:
        '''
        data = request.POST.copy()
        data['order'] = order_id

        form = PersonalDetailForm(data)

        context = {
            'personal_form': form,
            'order': order_id,
            'url': 'details',
            'is_form': True
        }

        if not request.user.is_authenticated():
            personal_info = PersonalInfoForm(data)
            context['personal_info'] = personal_info
            email = request.POST['email']
            context['email'] = email
            username = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            first_name = request.POST['first_name']
            context['first_name'] = first_name
            last_name = request.POST['last_name']
            context['last_name'] = last_name
            personal_info = PersonalInfoForm(data)

            if not password or not confirm_password or password != confirm_password:
                return render(request,
                              self.template_name,
                              context=context)

            try:
                user = User.objects.create_user(username, email, password)
                data['user'] = user.id
                if personal_info.is_valid():
                    personal_info.save()
                else:
                    return render(request,
                                  self.template_name,
                                  context=context)

                login(request, user)

                order = Order.objects.get(pk=order_id)
                order.user = user
                order.save()

            except IntegrityError:
                return render(request,
                              self.template_name,
                              context=context)

        if form.is_valid():
            form.save()
        else:
            return render(request,
                          self.template_name,
                          context=context)
        order = Order.objects.get(pk=order_id)
        order.user = request.user
        order.save()

        return HttpResponseRedirect(reverse('my_account'))


class DeleteOrder(View):
    def get(self, request, order_id=None):
        order = get_object_or_404(Order, id=order_id)
        if request.user != order.user and not request.user.is_superuser:
            return Http404()
        order.delete()
        return HttpResponseRedirect(reverse('my_account'))
