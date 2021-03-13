from rest_framework.pagination import LimitOffsetPagination


class ReviewPaginator(LimitOffsetPagination):
    max_limit = 3
