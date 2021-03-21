from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.reviews.models import Review
from apps.users.models import User


class ReviewViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'middle_name': 'test_middle_name',
            'phone': 'test_phone',
            'address': 'test_address',
        }
        self.user = User.objects.create(**self.user_data)

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('review')
        cls.review_data = {
            'text': 'test_text',
        }

    def test_unauthorized(self):
        response = self.client.post(self.url, data=self.review_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.review_data, format='json')
        review = Review.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                'id': 1,
                **self.review_data,
                'author': {
                    'id': 1,
                    'username': '',
                    **self.user_data,
                },
                'status': 'moderation',
                'created_at': review.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'published_at': None,
            },

        )
        self.assertEqual(
            model_to_dict(review),
            {
                'id': 1,
                **self.review_data,
                'author': self.user.id,
                'status': 'moderation',
                'published_at': None,
            },
        )


class ReviewViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
                email='test@example.com',
                first_name='test_first_name',
                last_name='test_last_name',
                middle_name='test_middle_name',
                phone='test_phone',
                address='test_address',
            )
        self.reviews = [
            Review.objects.create(
                text=f'test_text{i}',
                status=Review.Status.PUBLISHED,
                author=self.user,
            ) for i in range(10)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('review')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        reviews = Review.objects.all()
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        [self.assertEqual(
            data,
            {
                'id': review.id,
                'author': {
                    'id': review.author.id,
                    'username': review.author.username,
                    'email': review.author.email,
                    'first_name': review.author.first_name,
                    'last_name': review.author.last_name,
                    'middle_name': review.author.middle_name,
                    'phone': review.author.phone,
                    'address': review.author.address,
                },
                'status': review.status,
                'text': review.text,
                'created_at': review.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'published_at': review.published_at,
            },
        ) for data, review in zip(response.data, self.reviews)]
        [self.assertEqual(
            data,
            {
                'id': review.id,
                'author': {
                    'id': review.author.id,
                    'username': review.author.username,
                    'email': review.author.email,
                    'first_name': review.author.first_name,
                    'last_name': review.author.last_name,
                    'middle_name': review.author.middle_name,
                    'phone': review.author.phone,
                    'address': review.author.address,
                },
                'status': review.status,
                'text': review.text,
                'created_at': review.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'published_at': review.published_at,
            },
        ) for data, review in zip(response.data, reviews)]
