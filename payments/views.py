import requests
import os
from datetime import datetime, timedelta

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse

from orders.models import Order


# Create your views here.
class BasePayment(View):
    base_url = 'https://api.sandbox.paypal.com/v1/'

    def get_access_token(self, request, base_url):
        if 'expires_at' in request.session.keys() and \
                datetime.now() > request.session['expires_at'] + request.session['last_token'] or \
                'expires_at' not in request.session.keys():
            access_headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en_US',
            }

            auth = {os.environ.get('PAYPAL_APP_ID'): os.environ.get('PAYPAL_SECRET')}

            auth_result = requests.get(self.base_url + '/oauth2/token',
                                       auth=auth,
                                       headers=access_headers)
            result_json = auth_result.json()
            request.session['access_token'] = result_json['access_token']
            request.session['expires_at'] = timedelta(seconds=result_json['expires_in'])


class CreatePayment(BasePayment):
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
                        'total': order_price,
                        'currency': 'USD'
                    },
                    'items_list': {
                        'items': [
                            {
                                'quantity': 1,
                                'name': 'license',
                                'price': order_price,
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
            'Authorization': 'Bearer'
        }

        res = requests.post(self.base_url + 'payments/payment',
                            data=paypal,
                            headers=headers)
        return JsonResponse(res.json)


class ExecutePayment(BasePayment):
    def post(self, request):
        url = self.base_url + 'payments/payment/{0}/execute/'.format(request.POST['paymentID'])

        payment = {
            'payer_id': request.POST['payerID']
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer access_token$production$6xzb7s8y9ngf8mh9$76e737512b53650362681e5022a93946'
        }

        res = requests.post(url, data=payment, headers=headers)
        return JsonResponse(res.json())
