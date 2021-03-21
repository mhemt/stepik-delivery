from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import User


class UserDetailViewRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('user')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        user = get_user_model().objects.get()
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user, user)
        self.assertEqual(
            response.data,
            {
                'id': self.user.id,
                'username':  self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'middle_name': self.user.middle_name,
                'phone': self.user.phone,
                'address': self.user.address,
            },
        )


class UserDetailViewUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('user')
        cls.user_new_data = {
            'email': 'new_test@example.com',
            'first_name': 'new_test_first_name',
            'last_name': 'new_test_last_name',
            'middle_name': 'new_test_middle_name',
            'phone': 'new_test_phone',
            'address': 'new_test_address',
        }

    def test_put_unauthorized(self):
        response = self.client.put(self.url, data=self.user_new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url, data=self.user_new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_put(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.user_new_data, format='json')
        user = get_user_model().objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user_new_data,
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
            self.user_new_data,
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': user.middle_name,
                'phone': user.phone,
                'address': user.address,
            },
        )

    def test_patch(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, data=self.user_new_data, format='json')
        user = get_user_model().objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user_new_data,
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
            self.user_new_data,
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': user.middle_name,
                'phone': user.phone,
                'address': user.address,
            },
        )
