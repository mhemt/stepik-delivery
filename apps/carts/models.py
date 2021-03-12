from django.conf import settings
from django.db import models

from apps.items.models import Item


class Cart(models.Model):
    items = models.ManyToManyField(Item, through='CartItem', related_name='carts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')

    def __str__(self):
        return f'{self.user.username}\'s cart'

    @property
    def total_cost(self):
        return sum([item.total_price for item in self.cart_items.all()])


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ['item', 'cart']

    def __str__(self):
        return f'{self.cart.user.username}\'s {self.item.title}'

    @property
    def total_price(self):
        return self.quantity * self.price
