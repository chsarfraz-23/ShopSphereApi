from django.db.models import Q
from django_filters import rest_framework as filters

from Api.models.api_models import CartProductItem


class CartProductItemFilter(filters.FilterSet):
    search = filters.CharFilter(method="apply_search_filter")

    class Meta:
        model = CartProductItem
        fields = ["search"]

    def apply_search_filter(self, queryset, name, value):
        base_filter = Q(is_active=True, is_deleted=False)
        search_filters = (
                base_filter &
                Q(product__name__icontains=value) |
                Q(product__price__icontains=value) |
                Q(product__discount__icontains=value) |
                Q(product__type__name__icontains=value) |
                Q(product__phone_number__icontains=value) |
                Q(product__city__icontains=value) |
                Q(product__email__icontains=value) |
                Q(product__state=value)
        )
        return queryset.filter(search_filters)





