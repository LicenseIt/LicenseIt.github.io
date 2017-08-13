from django.db import models

from orders.models import Order


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RightType(Base):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'right type'
        verbose_name_plural = 'right types'


class OwnerDatabase(Base):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'owner'
        verbose_name_plural = 'owners'


class OrderOwnerRight(Base):
    owner = models.ForeignKey(OwnerDatabase, on_delete=models.SET_NULL, null=True, blank=True)
    right_type = models.ForeignKey(RightType, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.owner.name + ', ' + self.right_type.name + ', ' + self.order.song_title

    class Meta:
        verbose_name = 'owner right'
        verbose_name_plural = 'owner rights'


class Question(Base):
    question = models.CharField(max_length=400)
    answer = models.TextField(null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    owner = models.ForeignKey(OwnerDatabase, on_delete=models.CASCADE)

    def __str__(self):
        return self.question + ', ' + self.order.song_title

    class Meta:
        verbose_name = 'owner question'
        verbose_name_plural = 'owner questions'
