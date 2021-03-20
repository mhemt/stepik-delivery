from rest_framework import serializers
from rest_framework.fields import DecimalField, IntegerField

from apps.carts.models import Cart, CartItem
from apps.items.models import Item
from apps.items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    total_price = DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['item', 'item_id', 'price', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart_items', many=True)
    total_cost = DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']
        read_only_fields = ['items']


# TODO: fix wrong response
class PostItemToCartSerializer(serializers.Serializer):
    item_id = IntegerField()
    quantity = IntegerField()

    def create(self, validated_data):
        cart = self.context['request'].user.cart
        item = Item.objects.get(id=validated_data['item_id'])
        price = item.price
        quantity = validated_data['quantity']

        return CartItem.objects.create(
            item=item,
            cart=cart,
            price=price,
            quantity=quantity,
        )
