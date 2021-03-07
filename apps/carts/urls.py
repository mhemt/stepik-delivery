from django.urls import path

from apps.carts.views import CartDetailView

urlpatterns = [
    path('', CartDetailView.as_view(), name='carts'),
]
