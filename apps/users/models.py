from django.contrib.auth.models import AbstractUser
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from apps.carts.models import Cart


class User(AbstractUser):
    middle_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    @property
    def cart(self):
        try:
            cart, _ = Cart.objects.get_or_create(user=self)
        except MultipleObjectsReturned:
            cart = Cart.objects.filter(user=self).last()
        return cart
