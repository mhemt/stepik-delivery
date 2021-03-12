from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.carts.models import Cart


class User(AbstractUser):
    middle_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    @property
    def cart(self):
        cart, _ = Cart.objects.get_or_create(user=self)
        return cart
