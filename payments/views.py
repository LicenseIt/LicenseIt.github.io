from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
from requests.auth import HTTPBasicAuth
import logging
import json

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order
from .models import PaypalTokenData
from license_it import settings

log = logging.getLogger('payments')


class BasePayment(View):
    base_url = 'https://api.sandbox.paypal.com/v1/'
    base_live = 'https://api.paypal.com/v1/'

    def get_access_token(self, request):
        token = PaypalTokenData.objects.all()
        if not token or token[0].is_expired():
            url = self.base_live + 'oauth2/token'

            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en_US'
            }

            token_json = requests.post(url,
                                       headers=headers,
                                       params={'grant_type': 'client_credentials'},
                                       auth=(settings.PAYPAL_APP_ID, settings.PAYPAL_SECRET)).json()
            log.info(token_json)

            if token:
                token = token[0]
                token.access_token = token_json['access_token']
                token.expires_at = token_json['expires_in']
                token.save()
            else:
                token = PaypalTokenData()
                token.access_token = token_json['access_token']
                token.expires_in = token_json['expires_in']
                token.save()


@method_decorator(csrf_exempt, name='dispatch')
class CreatePayment(BasePayment):
    def post(self, request, order_id=None):
        order = Order.objects.get(pk=order_id)
        order_price = str(order.price)
        return_url = 'https://' + request.get_host() + reverse('my_account')

        paypal = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [
                {
                    "amount": {
                        "total": order_price, # 1.01
                        "currency": "USD",
                        "details": {
                            "subtotal": order_price,
                            "tax": "0.00",
                            "shipping": "0.00",
                            "handling_fee": "0.00",
                            "shipping_discount": "0.00",
                            "insurance": "0.00"
                        }
                    },
                    "description": "The payment transaction description.",
                    "invoice_number": "order{0}".format(order.id),
                    "payment_options": {
                        "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
                    },
                    "item_list": {
                        "items": [
                            {
                                "name": "license",
                                "description": "license for {0}.".format(order.song_title),
                                "quantity": "1",
                                "price": order_price,
                                "tax": "0.00",
                                "currency": "USD"
                            }
                        ]
                    }
                }
            ],
            "note_to_payer": "Contact us for any questions on your order.",
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": return_url
            }
        }

        self.get_access_token(request)
        access_token = 'Bearer {0}'.format(PaypalTokenData.objects.first().access_token)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        url = self.base_live + 'payments/payment'

        res = requests.post(url,
                            data=json.dumps(paypal),
                            headers=headers)
        res_json = res.json()

        request.session['payment_id'] = res_json['id']
        log.info(paypal['redirect_urls']['cancel_url'])
        return JsonResponse(res_json)


@method_decorator(csrf_exempt, name='dispatch')
class ExecutePayment(BasePayment):
    def post(self, request, order_id):
        log.info('get here!')
        url = self.base_live + 'payments/payment/{0}/execute/'.format(request.POST['paymentID'])
        log.info(url)

        self.get_access_token(request)
        access_token = "Bearer {0}".format(PaypalTokenData.objects.first().access_token)

        payment = {
            'payer_id': request.POST['payerID']
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        res = requests.post(url, data=json.dumps(payment), headers=headers)
        log.info(res.json())
        return JsonResponse(res.json())