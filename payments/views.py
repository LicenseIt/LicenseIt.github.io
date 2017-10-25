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
            log.info('in if')
            auth = HTTPBasicAuth(settings.PAYPAL_APP_ID, settings.PAYPAL_SECRET)
            client = BackendApplicationClient(client_id=settings.PAYPAL_APP_ID)
            oauth = OAuth2Session(client=client)
            log.info('before url')

            url = self.base_live + 'oauth2/token'

            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en_US'
            }

            token_json = requests.post(url,
                                       headers=headers,
                                       data={'grant_type': 'client_credentials'},
                                       auth=HTTPBasicAuth(settings.PAYPAL_APP_ID, settings.PAYPAL_SECRET)).json()
            log.info(token_json)
            log.info('after fe')

            if token:
                log.info('in token')
                token = token[0]
                token.access_token = token_json['access_token']
                token.expires_at = token_json['expires_in']
                token.save()
            else:
                log.info('in else')
                token = PaypalTokenData()
                token.access_token = token_json['access_token']
                log.info('access')
                token.expires_in = token_json['expires_in']
                log.info('expire')
                token.save()
                log.info('save')


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

        log.info('before access token')

        self.get_access_token(request)
        log.info('after access token')
        access_token = 'Bearer {0}'.format(PaypalTokenData.objects.first().access_token)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        url = self.base_live + 'payments/payment'
        log.info('before post to paypal')

        res = requests.post(url,
                            data=json.dumps(paypal),
                            headers=headers)
        log.info('after post')
        res_json = res.json()
        log.info(res_json)

        request.session['payment_id'] = res_json['id']
        log.info(res_json['id'])
        return JsonResponse(res_json)


class ExecutePayment(BasePayment):
    @method_decorator(csrf_exempt)
    def post(self, request):
        log.info('get here!')
        url = self.base_live + 'payments/payment/{0}/execute/'.format(request.POST['paymentID'])
        log.info(url)

        self.get_access_token(request)
        access_token = "Bearer {0}".format(request.session['access_token'])

        payment = {
            'payer_id': request.POST['payerID']
        }

        log.info(request.POST['payerID'])

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        res = requests.post(url, data=payment, headers=headers)
        return JsonResponse(res.json())
