from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.carts.models import Cart, CartItem
from apps.carts.paginators import CartItemPaginator
from apps.carts.serializers import CartSerializer, CartItemSerializer, PostItemToCartSerializer


class CartDetailView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user_id=self.request.user.id)


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    pagination_class = CartItemPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user_id=self.request.user.id)
        return self.queryset.filter(cart_id=cart.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostItemToCartSerializer
        else:
            return CartItemSerializer
