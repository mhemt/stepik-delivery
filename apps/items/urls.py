from django.urls import path

from apps.items.views import get_items_view

urlpatterns = [
    path('<int:pk>/', get_items_view),
]
