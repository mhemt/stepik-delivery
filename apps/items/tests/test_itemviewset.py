from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.items.models import Item
from apps.items.paginators import ItemPaginator


class ItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.items = [
            Item.objects.create(
                title=f'test_title{i}',
                description=f'test_description{i}',
                weight=1+i,
                price=Decimal(f'{199*i}.00'),
            ) for i in range(10)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('item-list')

    def test(self):
        items = Item.objects.all()
        response = self.client.get(self.url, format='json')

        start = 0
        page_size = ItemPaginator.page_size
        while True:
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(
                data['results'],
                [
                    {
                        'id': item.id,
                        'title': item.title,
                        'description': item.description,
                        'image': 'http://testserver/static/130x80.gif',
                        'weight': item.weight,
                        'price': str(item.price),
                    } for item in self.items[start:start+page_size]
                ],
            )
            if data['next']:
                response = self.client.get(data['next'], format='json')
                start += page_size
            else:
                break

        self.assertEqual(list(items), self.items)


class ItemViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.item = Item.objects.create(
            title='test_title',
            description='test_description',
            weight=10,
            price=Decimal('1999.00'),
        )
        self.url = reverse('item-detail', kwargs={'pk': self.item.id})

    def test(self):
        response = self.client.get(self.url)
        item = Item.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': self.item.id,
                'title': self.item.title,
                'description': self.item.description,
                'image': 'http://testserver/static/130x80.gif',
                'weight': self.item.weight,
                'price': str(self.item.price),
            },
        )
        self.assertEqual(item, self.item)
