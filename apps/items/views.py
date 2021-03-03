from rest_framework.viewsets import ModelViewSet

from apps.items.models import Item
from apps.items.serializers import ItemSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ['get']
