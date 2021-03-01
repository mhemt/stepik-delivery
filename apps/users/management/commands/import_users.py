import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL)

        for user in response.json():
            get_user_model().objects.get_or_create(
                id=user['id'],
                defaults={
                    'username': user['email'].split('@')[0],
                    'email': user['email'],
                    'password': make_password(user['password']),
                    'first_name': user['info']['name'],
                    'last_name': user['info']['surname'],
                    'middle_name': user['info']['patronymic'],
                    'phone': user['contacts']['phoneNumber'],
                    'address': user['city_kladr'],
                },
            )
