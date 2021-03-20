import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.carts.models import CartItem
from apps.items.models import Item


class CartItemViewSetListTestCase(APITestCase):
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
        cls.url = reverse('cart_item-list')

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
                'id': cart_item.id,
                'item': {
                    'id': cart_item.item.id,
                    'title': cart_item.item.title,
                    'description': cart_item.item.description,
                    'image': 'http://testserver/static/130x80.gif',
                    'weight': cart_item.item.weight,
                    'price': str(cart_item.item.price),
                },
                'item_id': cart_item.item.id,
                'quantity': cart_item.quantity,
                'price': str(cart_item.price),
                'total_price': str(cart_item.total_price),
            } for cart_item in self.user.cart.cart_items.all()],
        )


class CartItemViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('cart_item-list')
        cls.item = Item.objects.create(
                title='test_title',
                description='test_description',
                weight=10,
                price=Decimal('1999.00'),
        )
        cls.cart_item_data = {
            'item_id': cls.item.id,
            'quantity': random.randint(1, 10),
        }

    def test_unauthorized(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.cart_item_data, format='json')
        cart_item = CartItem.objects.get(cart=self.user.cart)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.cart_item_data, response.data)
        self.assertEqual(
            self.cart_item_data,
            {
                'item_id': cart_item.id,
                'quantity': cart_item.quantity,
            },
        )


class CartItemViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        self.item = Item.objects.create(
                title='test_title',
                description='test_description',
                weight=10,
                price=Decimal('1999.00'),
        )
        self.cart_item = CartItem.objects.create(
                cart=self.user.cart,
                item=self.item,
                quantity=random.randint(1, 10),
                price=self.item.price,
        )
        self.url = reverse('cart_item-detail', kwargs={'pk': self.cart_item.id})

    def test_unauthorized(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        cart_item = CartItem.objects.get(cart=self.user.cart)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': self.cart_item.id,
                'item': {
                    'id': self.cart_item.item.id,
                    'title': self.cart_item.item.title,
                    'description': self.cart_item.item.description,
                    'image': 'http://testserver/static/130x80.gif',
                    'weight': self.cart_item.item.weight,
                    'price': str(self.cart_item.item.price),
                },
                'item_id': self.cart_item.item.id,
                'quantity': self.cart_item.quantity,
                'price': str(self.cart_item.price),
                'total_price': str(self.cart_item.total_price),
            },
        )
        self.assertEqual(
            response.data,
            {
                'id': cart_item.id,
                'item': {
                    'id': cart_item.item.id,
                    'title': cart_item.item.title,
                    'description': cart_item.item.description,
                    'image': 'http://testserver/static/130x80.gif',
                    'weight': cart_item.item.weight,
                    'price': str(cart_item.item.price),
                },
                'item_id': cart_item.item.id,
                'quantity': cart_item.quantity,
                'price': str(cart_item.price),
                'total_price': str(cart_item.total_price),
            },
        )


class CartItemViewSetUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        cls.item = Item.objects.create(
                title='test_title',
                description='test_description',
                weight=10,
                price=Decimal('1999.00'),
        )
        cls.cart_item = CartItem.objects.create(
                cart=cls.user.cart,
                item=cls.item,
                quantity=2,
                price=cls.item.price,
        )
        cls.cart_item_data = {
            'quantity': 5,
        }
        cls.url = reverse('cart_item-detail', kwargs={'pk': cls.cart_item.id})

    def test_put_unauthorized(self):
        response = self.client.put(self.url, data=self.cart_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url, data=self.cart_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_put(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=self.cart_item_data)
        cart_item = CartItem.objects.get(cart=self.user.cart)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': cart_item.id,
                'item': {
                    'id': cart_item.item.id,
                    'title': cart_item.item.title,
                    'description': cart_item.item.description,
                    'image': 'http://testserver/static/130x80.gif',
                    'weight': cart_item.item.weight,
                    'price': str(cart_item.item.price),
                },
                'item_id': cart_item.item.id,
                'quantity': cart_item.quantity,
                'price': str(cart_item.price),
                'total_price': str(cart_item.total_price),
            },
        )

    def test_patch(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, data=self.cart_item_data)
        cart_item = CartItem.objects.get(cart=self.user.cart)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': cart_item.id,
                'item': {
                    'id': cart_item.item.id,
                    'title': cart_item.item.title,
                    'description': cart_item.item.description,
                    'image': 'http://testserver/static/130x80.gif',
                    'weight': cart_item.item.weight,
                    'price': str(cart_item.item.price),
                },
                'item_id': cart_item.item.id,
                'quantity': cart_item.quantity,
                'price': str(cart_item.price),
                'total_price': str(cart_item.total_price),
            },
        )


class CartItemViewSetDeleteTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            email='test@example.com',
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            phone='test_phone',
            address='test_address',
        )
        self.item = Item.objects.create(
                title='test_title',
                description='test_description',
                weight=10,
                price=Decimal('1999.00'),
        )
        self.cart_item = CartItem.objects.create(
                cart=self.user.cart,
                item=self.item,
                quantity=2,
                price=self.item.price,
        )
        self.url = reverse('cart_item-detail', kwargs={'pk': self.cart_item.id})

    def test_unauthorized(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url)
        self.assertIsNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
