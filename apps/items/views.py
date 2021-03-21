import json

from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.items.filters import ItemFilter
from apps.items.models import Item
from apps.items.paginators import ItemPaginator
from apps.items.serializers import ItemSerializer

ITEMS_CACHE_KEY = 'item_cache_key'
ITEMS_CACHE_TTL = 300


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPaginator
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ItemFilter

    def list(self, request, *args, **kwargs):
        cached_response = cache.get(ITEMS_CACHE_KEY)
        if cached_response:
            return Response(json.loads(cached_response))

        response = super().list(request, *args, **kwargs)
        cache.set(
            key=ITEMS_CACHE_KEY,
            value=json.dumps(response.data),
            timeout=ITEMS_CACHE_TTL,
        )
        return response
