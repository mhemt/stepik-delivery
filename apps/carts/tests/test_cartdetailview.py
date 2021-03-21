import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.carts.models import CartItem
from apps.items.models import Item


class CartDetailViewTestCase(APITestCase):
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
        cls.url = reverse('cart')

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
            {
                'id': self.user.cart.id,
                'items': [{
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
                'total_cost': str(self.user.cart.total_cost),
            },
        )
