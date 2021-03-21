from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.reviews.models import Review
from apps.reviews.paginators import ReviewPaginator
from apps.reviews.serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.select_related('author').filter(status=Review.Status.PUBLISHED)
