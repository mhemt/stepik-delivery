from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.carts.models import Cart


class Order(models.Model):

    class Status(models.TextChoices):
        CREATED = 'created', _('создан')
        DELIVERED = 'delivered', _('доставлен')
        PROCESSED = 'processed', _('в обработке')
        CANCELLED = 'cancelled', _('отменен')

    created_at = models.DateTimeField(auto_now_add=True)
    delivery_at = models.DateTimeField()
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=300)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.cart.user.username}\'s order from {self.created_at}'
