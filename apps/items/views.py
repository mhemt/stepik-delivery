from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.items.models import Item


@api_view(['GET'])
def get_items_view(request, pk):
    box_item = get_object_or_404(Item, id=pk)
    return Response({
        'id': box_item.id,
        'title': box_item.title,
        'description': box_item.description,
        'image': box_item.image.url,
        'weight': box_item.weight,
        'price': box_item.price,
    })
