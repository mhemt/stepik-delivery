from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.orders.models import Order
from apps.orders.paginators import OrderPaginator
from apps.orders.serializers import OrderSerializer, PostOrderSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pagination_class = OrderPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(cart=self.request.user.cart)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostOrderSerializer
        else:
            return OrderSerializer
