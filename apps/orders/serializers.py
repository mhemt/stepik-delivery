from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField

from apps.carts.serializers import CartSerializer
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'cart', 'status', 'recipient', 'total_cost', 'address', 'delivery_at', 'created_at']
        read_only_fields = ['recipient', 'cart', 'total_cost', 'created_at']
        extra_kwargs = {
            'status': {'required': False},
            'address': {'required': False},
            'delivery_at': {'required': False},
        }


class PostOrderSerializer(serializers.Serializer):
    address = CharField()
    delivery_at = DateTimeField()

    def create(self, validated_data):
        delivery_at = validated_data['delivery_at']
        recipient = self.context['request'].user
        address = validated_data['address']
        cart = self.context['request'].user.cart
        status = Order.Status.CREATED
        total_cost = cart.total_cost

        return Order.objects.create(
            delivery_at=delivery_at,
            recipient=recipient,
            address=address,
            cart=cart,
            status=status,
            total_cost=total_cost,
        )
