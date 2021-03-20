from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.carts.models import CartItem
from apps.carts.paginators import CartItemPaginator
from apps.carts.serializers import CartSerializer, CartItemSerializer, PostItemToCartSerializer


class CartDetailView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.cart


class CartItemViewSet(ModelViewSet):
    pagination_class = CartItemPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostItemToCartSerializer
        else:
            return CartItemSerializer
