from datetime import datetime, timedelta

from django.db import models


class PaypalTokenData(models.Model):
    access_token = models.CharField(max_length=200)
    expires_in = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return datetime.now() > self.updated + timedelta(seconds=self.expires_in)
