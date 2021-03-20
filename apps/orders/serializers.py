from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'cart', 'status', 'total_cost', 'address', 'delivery_at', 'created_at']
        read_only_fields = ['cart', 'total_cost', 'created_at']
        extra_kwargs = {
            'status': {'required': False},
            'address': {'required': False},
            'delivery_at': {'required': False},
        }

    def validate(self, data):
        current_status = Order.objects.filter(recipient=self.context['request'].user).last().status
        new_status = data.get('status')

        if current_status == Order.Status.CREATED:
            if new_status and new_status != Order.Status.CANCELLED:
                raise serializers.ValidationError('You can change your status only to cancelled')
            return data
        else:
            raise serializers.ValidationError('You can\'t change your order anymore')


class CreateOrderSerializer(serializers.Serializer):
    address = CharField()
    delivery_at = DateTimeField()

    def create(self, validated_data):
        delivery_at = validated_data['delivery_at']
        recipient = self.context['request'].user
        address = validated_data['address']
        cart = recipient.cart
        total_cost = cart.total_cost

        return Order.objects.create(
            delivery_at=delivery_at,
            recipient=recipient,
            address=address,
            cart=cart,
            total_cost=total_cost,
        )
