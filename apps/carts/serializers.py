from rest_framework import serializers

from apps.carts.models import Cart, CartItem
from apps.items.serializers import ItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
        ]


