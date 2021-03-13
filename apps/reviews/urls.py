from django.urls import path

from apps.reviews.views import ReviewView

urlpatterns = [
    path('', ReviewView.as_view(), name='review'),
]
