import random
from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.carts.models import CartItem
from apps.items.models import Item
from apps.orders.models import Order


class OrderViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        items = [
            Item.objects.create(
                title=f'test_title{i}',
                description=f'test_description{i}',
                weight=1+i,
                price=Decimal(f'{199*i}.00'),
            ) for i in range(10)
        ]
        self.items = random.sample(items, random.randint(1, len(items)))
        for item in self.items:
            CartItem.objects.create(
                cart=self.user.cart,
                item=item,
                quantity=random.randint(1, 10),
                price=item.price,
            )
            Order.objects.create(
                delivery_at=datetime.now(tz=timezone.utc),
                recipient=self.user,
                address='delivery_address',
                cart=self.user.cart,
                status=random.choice(Order.Status.values),
                total_cost=self.user.cart.total_cost,
            )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('order-list')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [{
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            } for order in Order.objects.filter(recipient=self.user)],
        )


class OrderViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        items = [
            Item.objects.create(
                title=f'test_title{i}',
                description=f'test_description{i}',
                weight=1+i,
                price=Decimal(f'{199*i}.00'),
            ) for i in range(10)
        ]
        self.items = random.sample(items, random.randint(1, len(items)))
        for item in self.items:
            CartItem.objects.create(
                cart=self.user.cart,
                item=item,
                quantity=random.randint(1, 10),
                price=item.price,
            )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('order-list')
        cls.order_data = {
            'delivery_at': datetime.now(tz=timezone.utc),
            'address': 'delivery_address',
        }

    def test_unauthorized(self):
        response = self.client.post(self.url, data=self.order_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.order_data, format='json')
        order = Order.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },

        )
        self.assertEqual(
            self.order_data,
            {
                'delivery_at': order.delivery_at,
                'address': order.address,
            },
        )


class OrderViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        items = [
            Item.objects.create(
                title=f'test_title{i}',
                description=f'test_description{i}',
                weight=1+i,
                price=Decimal(f'{199*i}.00'),
            ) for i in range(10)
        ]
        self.items = random.sample(items, random.randint(1, len(items)))
        for item in self.items:
            CartItem.objects.create(
                cart=self.user.cart,
                item=item,
                quantity=random.randint(1, 10),
                price=item.price,
            )
        self.order = Order.objects.create(
            delivery_at=datetime.now(tz=timezone.utc),
            recipient=self.user,
            address='delivery_address',
            cart=self.user.cart,
            total_cost=self.user.cart.total_cost,
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.id})

    def test_unauthorized(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        order = Order.objects.get(recipient=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(order, self.order)
        self.assertEqual(
            response.data,
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )


class OrderViewSetUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        items = [
            Item.objects.create(
                title=f'test_title{i}',
                description=f'test_description{i}',
                weight=1+i,
                price=Decimal(f'{199*i}.00'),
            ) for i in range(10)
        ]
        self.items = random.sample(items, random.randint(1, len(items)))
        for item in self.items:
            CartItem.objects.create(
                cart=self.user.cart,
                item=item,
                quantity=random.randint(1, 10),
                price=item.price,
            )
        self.order = Order.objects.create(
            delivery_at=datetime.now(tz=timezone.utc),
            recipient=self.user,
            address='delivery_address',
            cart=self.user.cart,
            total_cost=self.user.cart.total_cost,
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.id})

    @classmethod
    def setUpTestData(cls):
        cls.order_data = {
            'address': 'new_delivery_address',
            'delivery_at': datetime.now(tz=timezone.utc),
        }
        cls.order_data2 = {
            'status': Order.Status.DELIVERED,
        }
        cls.order_data3 = {
            'status': Order.Status.CANCELLED,
        }

    def test_put_unauthorized(self):
        response = self.client.put(self.url, data=self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url, data=self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_put(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.order_data, format='json')
        order = Order.objects.get(recipient=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )
        self.assertEqual(
            {
                'id': self.order.id,
                'cart': self.order.cart.id,
                'status': self.order.status,
                'total_cost': str(self.order.total_cost),
                'address': self.order_data['address'],
                'delivery_at': self.order_data['delivery_at'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': self.order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

        response = self.client.put(self.url, data=self.order_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': ['You can change your status only to cancelled']})

        response = self.client.put(self.url, data=self.order_data3, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': self.order_data3['status'],
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

        response = self.client.put(self.url, data=self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': ['You can\'t change your order anymore']})

    def test_patch(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, data=self.order_data, format='json')
        order = Order.objects.get(recipient=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )
        self.assertEqual(
            {
                'id': self.order.id,
                'cart': self.order.cart.id,
                'status': self.order.status,
                'total_cost': str(self.order.total_cost),
                'address': self.order_data['address'],
                'delivery_at': self.order_data['delivery_at'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': self.order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': order.status,
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

        response = self.client.patch(self.url, data=self.order_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': ['You can change your status only to cancelled']})

        response = self.client.patch(self.url, data=self.order_data3, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': order.id,
                'cart': order.cart.id,
                'status': self.order_data3['status'],
                'total_cost': str(order.total_cost),
                'address': order.address,
                'delivery_at': order.delivery_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_at': order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

        response = self.client.patch(self.url, data=self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': ['You can\'t change your order anymore']})
