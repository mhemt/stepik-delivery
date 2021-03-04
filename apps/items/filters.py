import django_filters

from apps.items.models import Item


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'price': ['gt', 'gte', 'lt', 'lte'],
            'weight': ['gt', 'gte', 'lt', 'lte'],
        }