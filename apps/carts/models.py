from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F, DecimalField

from apps.items.models import Item


class Cart(models.Model):
    items = models.ManyToManyField(Item, through='CartItem', related_name='carts')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='carts')

    def __str__(self):
        return f'{self.user.username}"s cart'

    @property
    def total_cost(self):
        total_cost = self.items.aggregate(
            total_cost=Sum(
                F('cartitem__quantity') * F('cartitem__price'),
                output_field=DecimalField(max_digits=8, decimal_places=2)
            )
        )['total_cost']

        return str(total_cost)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.price
