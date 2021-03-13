from rest_framework.pagination import LimitOffsetPagination


class OrderPaginator(LimitOffsetPagination):
    max_limit = 3
