import requests
from django.core.management import BaseCommand

from apps.items.models import Item

URL = 'https://stepik.org/media/attachments/course/73594/beautyboxes.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL)

        for box_item in response.json():
            Item.objects.get_or_create(
                id=box_item['id'],
                defaults={
                    'title': box_item['title'],
                    'description': box_item['description'],
                    'image': box_item['image'],
                    'weight': box_item['weight_grams'],
                    'price': box_item['price'],
                },
            )
