from django.contrib.auth import get_user_model
from django.db import models


class Review(models.Model):
    STATUS_CHOICES = [
        ('moderation', 'на модерации'),
        ('published', 'опубликован'),
        ('rejected', 'отклонен'),
    ]
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField()
    published_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.text
