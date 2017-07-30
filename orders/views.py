from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from search.models import Search, Track, Collection, Artist
from .models import Order #, OrderAdvertising, OrderIndie, OrderProgram, OrderWedding
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
        form = OrderIndieForm()
        return render(request,
                      'orders/order_indie.html',
                      context={'form': form, 'pk': pk, 'order': order_id})

    def post(self, request, pk, order_id):
        form = OrderIndieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        return render(request,
                      'orders/order_indie.html',
                      context={'form': form, 'pk': pk, 'order': order_id}
                      )


# class OrderAdView(View):
#     def get(self, request, pk, order_id):
#         form = OrderAdvertiseForm()
#         return render(request,
#                       'orders/order_ad.html',
#                       context={'form': form, 'pk': pk, 'order': order_id})
#
#     def post(self, request, pk, order_id):
#         form = OrderAdvertiseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('home'))
#         return render(request,
#                       'orders/order_ad.html',
#                       context={'form': form, 'pk': pk, 'order': order_id}
#                       )
#
#
# class OrderProgramView(View):
#     def get(self, request, pk, order_id):
#         form = OrderProgramForm()
#         return render(request,
#                       'orders/order_program.html',
#                       context={'form': form, 'pk': pk, 'order': order_id})
#
#     def post(self, request, pk, order_id):
#         form = OrderProgramForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('home'))
#         return render(request,
#                       'orders/order_program.html',
#                       context={'form': form, 'pk': pk, 'order': order_id}
#                       )
#
#
# class OrderWeddingView(View):
#     def get(self, request, pk, order_id):
#         form = OrderWeddingForm()
#         return render(request,
#                       'orders/order_wedding.html',
#                       context={'form': form, 'pk': pk, 'order': order_id})
#
#     def post(self, request, pk, order_id):
#         form = OrderWeddingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('home'))
#         return render(request,
#                       'orders/order_wedding.html',
#                       context={'form': form, 'pk': pk, 'order': order_id}
#                       )
