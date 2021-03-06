from rest_framework.pagination import LimitOffsetPagination


class CartItemPaginator(LimitOffsetPagination):
    max_limit = 3
