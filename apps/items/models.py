from django.db import models

from stepik_delivery.settings import STATIC_ROOT


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=STATIC_ROOT, default='static/130x80.gif')
    weight = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
