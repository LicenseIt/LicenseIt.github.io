import requests
import os
from datetime import datetime, timedelta
import logging
import base64

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse

from orders.models import Order
from .models import PaypalTokenData
from license_it import settings

log = logging.getLogger('payments')


class BasePayment(View):
    base_url = 'https://api.sandbox.paypal.com/v1/'

    def get_access_token(self, request):
        token = PaypalTokenData.objects.all()
        if not token or token[0].is_expired():
            access_headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en_US'
            }

            auth = (settings.PAYPAL_APP_ID, settings.PAYPAL_SECRET)

            url = self.base_url + 'oauth2/token'

            auth_result = requests.get(url,
                                       auth=auth,
                                       data={'grant_type': 'client_credentials'},
                                       headers=access_headers)
            result_json = auth_result.json()
            if token:
                token = token[0]
                token.access_token = result_json['access_token']
                token.expires_at = result_json['expires_in']
                token.save()
            else:
                token = PaypalTokenData()
                token.access_token = result_json['access_token']
                token.expires_in = result_json['expires_in']
                token.save()


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
                                'tax': 0
                            }
                        ]
                    }
                }
            ]
        }

        self.get_access_token(request)
        access_token = 'Bearer {0}'.format(PaypalTokenData.objects.first().access_token)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        res = requests.post(self.base_url + 'payments/payment',
                            data=paypal,
                            headers=headers)
        return JsonResponse(res.json)


class ExecutePayment(BasePayment):
    def post(self, request):
        url = self.base_url + 'payments/payment/{0}/execute/'.format(request.POST['paymentID'])

        self.get_access_token(request)
        access_token = "Bearer {0}".format(request.session['access_token'])

        payment = {
            'payer_id': request.POST['payerID']
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        res = requests.post(url, data=payment, headers=headers)
        return JsonResponse(res.json())
