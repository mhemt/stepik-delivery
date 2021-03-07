from django.contrib.auth import get_user_model
from django.db import models

from apps.items.models import Item


class Cart(models.Model):
    items = models.ManyToManyField(Item, through='CartItem', related_name='carts')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='carts')

    def __str__(self):
        return f'{self.user.username}"s cart'

    @property
    def total_cost(self):
        items = self.cart_items.all()
        return sum([item.total_price for item in items])


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.price

    @property
    def total_price(self):
        return self.quantity * self.price
