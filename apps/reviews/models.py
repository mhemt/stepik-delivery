from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):

    class Status(models.TextChoices):
        MODERATION = 'moderation', _('на модерации')
        PUBLISHED = 'published', _('опубликован')
        REJECTED = 'rejected', _('отклонен')

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MODERATION)

    def __str__(self):
        return self.text
