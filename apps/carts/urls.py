from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.carts.views import CartDetailView, CartItemViewSet

router = DefaultRouter()
router.register('items', CartItemViewSet, basename='cart_item')

urlpatterns = [
    path('', CartDetailView.as_view()),
    path('', include(router.urls)),
]