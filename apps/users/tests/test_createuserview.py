from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import User


class CreateUserViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('register')
        cls.user_data = {
            'email': 'test@example.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'middle_name': 'test_middle_name',
            'phone': 'test_phone',
            'address': 'test_address',
        }

    def test(self):
        response = self.client.post(self.url, data=self.user_data, format='json')
        user = User.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.user_data,
            {
                'email': response.data['email'],
                'first_name': response.data['first_name'],
                'last_name': response.data['last_name'],
                'middle_name': response.data['middle_name'],
                'phone': response.data['phone'],
                'address': response.data['address'],
            },
        )
        self.assertEqual(
            self.user_data,
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': user.middle_name,
                'phone': user.phone,
                'address': user.address,
            },
        )
