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

from owners.models import OrderOwnerRight, OwnerDatabase, RightType

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
            web_form.save()

        if ext_form:
            ext_form.save()

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
        if 'tv_trailer' in request.POST or 'tv_program' in request.POST:
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
            web_form.save()

        if ext_form:
            ext_form.save()

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
        if 'externally' in dist_list:
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
        order = Order.objects.get(pk=order_id)

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
            web_form.save()

        if ext_form:
            ext_form.save()

        # if tv_form:
        #     tv_form.save()

        return HttpResponseRedirect(reverse('advertising_details', args=[order_id]))


class DetailBase(View):
    def add_onwners(self, order_id=None):
        order_rights = {
            'composition': 'composition owner',
            'lirics': 'lyrics owner',
            'performance': 'performance owner'
        }

        order = Order.objects.get(pk=order_id)

        for right, owner in order_rights.items():
            order_owner_right = OrderOwnerRight()
            order_owner_right.order = order
            right = RightType.objects.get(name=right)
            order_owner_right.right_type = right
            owner = OwnerDatabase.objects.get(name=owner)
            order_owner_right.owner = owner
            order_owner_right.save()

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

        if form.is_valid():
            form.save()
            order = Order.objects.get(pk=order_id)
            order.is_done = True
            order.save()
        else:
            return render(request,
                          self.template_name,
                          context=context)

        order = Order.objects.get(pk=order_id)
        if request.user.is_authenticated():
            order.user = request.user
            order.save()
            if 'rate' in request.POST:
                return HttpResponseRedirect(reverse('my_account'))

        if 'rate' in request.POST:
            request.session['order_id'] = order_id
            return HttpResponseRedirect(reverse('login'))
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
        self.add_onwners(order_id)
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

        order_dist = OrderProgramming.objects.filter(order=order_id)[0]
        dist_list = [dist.__str__().lower() for dist in order_dist.distribution.all()]

        context = {
            'details_form': form,
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
        self.add_onwners(order_id)
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

        context = {
            'details_form': form,
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
        self.add_onwners(order_id)
        return self.func(request, order_id, AdvertisingDetailForm)


class RateUsView(View):
    '''
    the view for a rate us page if we have only 3 forms on indie, programming or advertising
    '''
    template_name = 'orders/rate_us_form.html'

    def get(self, request, order_id):
        '''
        rate us page
        :param request: request object
        :param order_id: the order id
        :return: rate us page
        '''
        rate_form = RateUsForm()
        return render(request,
                      self.template_name,
                      context={'rate_form': rate_form, 'order': order_id, 'is_form': True})

    def post(self, request, order_id):
        '''
        save the data of rate us form
        :param request: request object
        :param order_id: order id
        :return: login page or client dash page
        '''
        rate_form = RateUsForm(request.POST.copy())
        rate_form.data['order'] = order_id

        if rate_form.is_valid():
            rate_form.save()
        else:
            return render(request,
                          self.template_name,
                          context={'rate_form': rate_form, 'order': order_id, 'is_form': True})

        if request.user.is_authenticated():
            order = Order.objects.get(pk=order_id)
            order.user = request.user
            order.save()
            return HttpResponseRedirect(reverse('my_account'))
        else:
            request.session['order_id'] = order_id
            return HttpResponseRedirect(reverse('login'))


class WeddingDetails(View):
    '''
    the wedding details form view
    '''
    template_name = 'orders/wedding_detail.html'

    def add_onwners(self, order=None):
        order_rights = {
            'composition': 'composition owner',
            'lirics': 'lirics owner',
            'performance': 'performance owner'
        }

        for right, owner in order_rights.items():
            order_owner_right = OrderOwnerRight()
            order_owner_right.order = order
            right = RightType.objects.get(name=right)
            order_owner_right.right_type = right
            owner = OwnerDatabase.objects.get(name=owner)
            order_owner_right.owner = owner
            order_owner_right.save()

    def get(self, request, order_id):
        '''
        get the page
        :param request: the request object
        :param order_id: the order id
        :return:
        '''
        form = WeddingDetailForm()

        return render(request,
                      self.template_name,
                      context={
                          'wedding_form': form,
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

        if form.is_valid():
            form.save()
            order = Order.objects.get(pk=order_id)
            order.is_done = True
            order.save()
        else:
            return render(request,
                          self.template_name,
                          context=context)

        order = Order.objects.get(pk=order_id)
        self.add_onwners(order)
        if request.user.is_authenticated():
            order.user = request.user
            order.save()
            return HttpResponseRedirect(reverse('my_account'))

        request.session['order_id'] = order_id
        return HttpResponseRedirect(reverse('login'))


class PersonalDetails(View):
    '''
    the personal details form view
    '''
    template_name = 'orders/personal_detail.html'

    def add_onwners(self, order=None):
        order_rights = {
            'composition': 'composition owner',
            'lirics': 'lirics owner',
            'performance': 'performance owner'
        }

        for right, owner in order_rights.items():
            order_owner_right = OrderOwnerRight()
            order_owner_right.order = order
            right = RightType.objects.get(name=right)
            order_owner_right.right_type = right
            owner = OwnerDatabase.objects.get(name=owner)
            order_owner_right.owner = owner
            order_owner_right.save()

    def get(self, request, order_id):
        '''
        get the page
        :param request: request object
        :param order_id: order id
        :return:
        '''
        form = PersonalDetailForm()

        return render(request,
                      self.template_name,
                      context={
                          'personal_form': form,
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

        if form.is_valid():
            form.save()
        else:
            return render(request,
                          self.template_name,
                          context=context)

        order = Order.objects.get(pk=order_id)
        order.is_done = True
        order.save()

        self.add_onwners(order)

        if request.user.is_authenticated():
            order.user = request.user
            order.save()
            return HttpResponseRedirect(reverse('my_account'))

        request.session['order_id'] = order_id
        return HttpResponseRedirect(reverse('login'))


class DeleteOrder(View):
    '''
    delete order from client dash
    '''
    def get(self, request, order_id=None):
        '''
        deleting order from client dash page
        :param request: request object
        :param order_id: order id (to delete)
        :return: client dash if successful, 404 otherwise
        '''
        order = get_object_or_404(Order, id=order_id)
        if request.user != order.user and not request.user.is_superuser:
            return Http404()
        order.delete()
        return HttpResponseRedirect(reverse('my_account'))
