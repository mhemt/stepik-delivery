from rest_framework import serializers

from apps.carts.models import Cart, CartItem
from apps.items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    # item_id = serializers.IntegerField(source='item.id')
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, obj):
        return str(obj.quantity * obj.price)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'item',
            'item_id',
            'quantity',
            'price',
            'total_price',
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_cost',
        ]
