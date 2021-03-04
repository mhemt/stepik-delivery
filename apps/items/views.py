from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from apps.items.filters import ItemFilter
from apps.items.models import Item
from apps.items.paginators import ItemPaginator
from apps.items.serializers import ItemSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ['get']
    pagination_class = ItemPaginator
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ItemFilter
