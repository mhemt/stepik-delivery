from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.carts.models import Cart, CartItem
from apps.carts.paginators import CartItemPaginator
from apps.carts.serializers import CartSerializer, CartItemSerializer


class CartViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['get']
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.queryset.filter(user_id=self.request.user.id)


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = CartItemPaginator

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    #
    # def get_queryset(self):
    #     return self.queryset.filter(user_id=self.request.user.id)
