from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# from .models import Search, Track, Collection, Artist


class OrderView(View):
    '''
    The order page
    '''
    def get(self, request, *args, **kwargs):
        '''
        Return the order page
        :param request:
        :return:
        '''
        return render(request, 'orders/order.html')


class OrderListView(View):
    def get(self, request):
        order_list = []
        return render(request, 'orders/order_list.html', {'order_list': order_list})
