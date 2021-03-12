from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.items.filters import ItemFilter
from apps.items.models import Item
from apps.items.paginators import ItemPaginator
from apps.items.serializers import ItemSerializer


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPaginator
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ItemFilter
