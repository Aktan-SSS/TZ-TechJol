from django_filters import rest_framework as filters
from .models import Product


class ProductFilterSet(filters.FilterSet):
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    brand = filters.ChoiceFilter(choices=Product.objects.values_list('brand', 'brand').distinct())
    category = filters.ChoiceFilter(choices=Product.objects.values_list('category', 'category').distinct())

    class Meta:
        model = Product
        fields = ['brand', 'category', 'min_price', 'max_price']
