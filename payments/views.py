from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
from requests.auth import HTTPBasicAuth
import logging
import json

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator

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

            auth = HTTPBasicAuth(settings.PAYPAL_APP_ID, settings.PAYPAL_SECRET)
            client = BackendApplicationClient(client_id=settings.PAYPAL_APP_ID)
            oauth = OAuth2Session(client=client)

            url = self.base_url + 'oauth2/token'

            token_json = oauth.fetch_token(token_url=url, auth=auth)
            log.info(token)

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


class CreatePayment(BasePayment):
    @method_decorator(csrf_exempt)
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
                "return_url": "https://www.licenseit.net/accounts/my_account/",
                "cancel_url": "https://www.licenseit.net/accounts/my_account/"
            }
        }

        self.get_access_token(request)
        access_token = 'Bearer {0}'.format(PaypalTokenData.objects.first().access_token)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        log.info(json.dumps(paypal))

        res = requests.post(self.base_url + 'payments/payment',
                            data=json.dumps(paypal),
                            headers=headers)
        log.info(res.json())
        return JsonResponse(res.json())


class ExecutePayment(BasePayment):
    @method_decorator(csrf_exempt)
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
