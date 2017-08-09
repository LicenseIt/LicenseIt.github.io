from django.db import models

from orders.models import Order


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnerDatabase(Base):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(Base):
    question = models.CharField(max_length=400)
    answer = models.TextField(null=True, blank=True)
    seen_by_user = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    owner = models.ForeignKey(OwnerDatabase, on_delete=models.CASCADE)
