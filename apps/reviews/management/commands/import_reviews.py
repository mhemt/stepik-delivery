import requests
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.reviews.models import Review

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL)

        for review in response.json():
            user = get_user_model().objects.get(id=review['author'])
            Review.objects.get_or_create(
                id=review['id'],
                defaults={
                    'author': user,
                    'text': review['content'],
                    'created_at': review['created_at'],
                    'published_at': review['published_at'] if review['published_at'] != '' else None,
                    'status': review['status'],
                },
            )
