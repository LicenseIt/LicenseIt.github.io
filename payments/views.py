import requests

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse

from orders.models import Order


# Create your views here.
class CreatePayment(View):
    def post(self, request, order_id=None):
        order_price = Order.objects.get(pk=order_id).price
        paypal = {
            'intent': 'sale',
            'redirect_urls': {
                'return_url': reverse('my_account'),
                'cancel_url': reverse('my_account')
            },
            'payer': {
                'payment_method': 'paypal'
            },
            'transactions': [
                {
                    'ammount': {
                        'total': '0.01',
                        'currency': 'USD'
                    },
                    'items_list': {
                        'items': [
                            {
                                'quantity': 1,
                                'name': 'license',
                                'price': '0.01',
                                'currency': 'USD',
                                'description': 'license price',
                                'tax': '0'
                            }
                        ]
                    }
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'access_token$production$6xzb7s8y9ngf8mh9$76e737512b53650362681e5022a93946'
        }

        res = requests.post('https://api.sandbox.paypal.com/v1/payments/payment',
                            data=paypal,
                            headers=headers)
        print(res)
        return JsonResponse(res.json())


class ExecutePayment(View):
    def post(self, request):
        url = 'https://api.sandbox.paypal.com/v1/payments/payment/{0}/execute/'.format(request.POST['paymentID'])

        payment = {
            'payer_id': request.POST['payerID']
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer access_token$production$6xzb7s8y9ngf8mh9$76e737512b53650362681e5022a93946'
        }

        res = requests.post(url, data=payment, headers=headers)
        return JsonResponse(res.json())
