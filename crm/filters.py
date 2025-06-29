import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name_Icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email_Icontains = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    created_at_Gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_Lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    phone_Prefix = django_filters.CharFilter(method='filter_phone_prefix')

    class Meta:
        model = Customer
        fields = ['name_Icontains', 'email_Icontains', 'created_at_Gte', 'created_at_Lte', 'phone_Prefix']

    def filter_phone_prefix(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)


class ProductFilter(django_filters.FilterSet):
    name_Icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price_Gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_Lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock_Gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_Lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name_Icontains', 'price_Gte', 'price_Lte', 'stock_Gte', 'stock_Lte']


class OrderFilter(django_filters.FilterSet):
    total_amount_Gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_Lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date_Gte = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    order_date_Lte = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')
    customer_name_Icontains = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name_Icontains = django_filters.CharFilter(method='filter_product_name')
    product_id = django_filters.NumberFilter(method='filter_product_id')

    class Meta:
        model = Order
        fields = ['total_amount_Gte', 'total_amount_Lte', 'order_date_Gte', 'order_date_Lte', 'customer_name_Icontains']

    def filter_product_name(self, queryset, name, value):
        return queryset.filter(products__name__icontains=value).distinct()

    def filter_product_id(self, queryset, name, value):
        return queryset.filter(products__id=value).distinct()
