from rest_framework.viewsets import ModelViewSet

from apps.carts.models import Cart
from apps.carts.serializers import CartSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['get']