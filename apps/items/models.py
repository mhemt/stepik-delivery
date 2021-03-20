from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from stepik_delivery.settings import STATIC_ROOT


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=STATIC_ROOT, default='static/130x80.gif')
    weight = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


@receiver([post_save, post_delete], sender=Item)
def invalidate_item_cache(sender, instance, **kwargs):
    from apps.items.views import ITEMS_CACHE_KEY
    cache.delete(ITEMS_CACHE_KEY)
