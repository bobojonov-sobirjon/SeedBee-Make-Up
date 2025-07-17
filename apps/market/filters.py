import django_filters
from django.db.models import Q, Avg
from django_filters import rest_framework as filters
from apps.market.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    # Search filter - searches in all language translations
    search = django_filters.CharFilter(method='filter_search', label='Search by product name in any language')
    
    # Category filter
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        label='Filter by category'
    )
    
    # Brand filter
    brand = django_filters.CharFilter(
        field_name='brand',
        lookup_expr='icontains',
        label='Filter by brand name'
    )
    
    # Price range filters
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Minimum price'
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maximum price'
    )
    
    # Color filter
    color = django_filters.CharFilter(method='filter_color', label='Filter by color hex code')
    
    # Rating filter
    min_rating = django_filters.NumberFilter(method='filter_rating', label='Minimum average rating')
    
    # Additional useful filters
    has_discount = django_filters.BooleanFilter(method='filter_has_discount', label='Has discount price')
    
    # Price range filter (alternative approach)
    price_range = django_filters.RangeFilter(field_name='price', label='Price range')

    is_popular = django_filters.BooleanFilter(
        field_name='is_popular',
        label='Filter popular products',
        method='filter_is_popular'
    )

    is_new = django_filters.BooleanFilter(
        field_name='is_new',
        label='Filter new products',
        method='filter_is_new'
    )

    is_discounted = django_filters.BooleanFilter(
        field_name='is_discounted',
        label='Filter products with discount price',
        method='filter_is_discounted'
    )

    def filter_is_popular(self, queryset, name, value):
        """Filter popular products"""
        if value is True:
            return queryset.filter(is_popular=True)
        elif value is False:
            return queryset.filter(is_popular=False)
        return queryset

    def filter_is_new(self, queryset, name, value):
        """Filter new products"""
        if value is True:
            return queryset.filter(is_new=True)
        elif value is False:
            return queryset.filter(is_new=False)
        return queryset

    def filter_is_discounted(self, queryset, name, value):
        """Filter products that have a discount price"""
        if value is True:
            return queryset.filter(is_discounted=True)
        elif value is False:
            return queryset.filter(is_discounted=False)
        return queryset

    # Ordering
    ordering = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('price', 'price'),
            ('id', 'id'),
        ),
        field_labels={
            'created_at': 'Date Created',
            'price': 'Price',
            'id': 'ID',
        }
    )

    class Meta:
        model = Product
        fields = {
            'price': ['exact', 'gte', 'lte'],
            'brand': ['exact', 'icontains'],
            'category': ['exact'],
        }

    def filter_search(self, queryset, name, value):
        """Filter by product name in all language translations"""
        if not value:
            return queryset
        
        search_q = Q()
        # Search in translated names for all languages
        for lang_code in ['ru', 'en', 'uz', 'kk', 'ko']:
            search_q |= Q(
                **{f'translations__name__icontains': value, 
                   f'translations__language_code': lang_code}
            )
        
        return queryset.filter(search_q).distinct()

    def filter_color(self, queryset, name, value):
        """Filter by color hex code"""
        if not value:
            return queryset
        
        # Remove # if present and validate hex color
        color = value.lstrip('#')
        
        # Handle both 6-character (#RRGGBB) and 8-character (#RRGGBBAA) hex codes
        if len(color) == 6:
            # Standard 6-character hex color
            try:
                int(color, 16)  # Validate hex
                return queryset.filter(colors__color__icontains=color).distinct()
            except ValueError:
                # Invalid hex color - return empty queryset
                return queryset.none()
        elif len(color) == 8:
            # 8-character hex color with alpha - use only RGB part (first 6 characters)
            try:
                rgb_part = color[:6]  # Take only RGB, ignore alpha
                int(rgb_part, 16)  # Validate hex
                return queryset.filter(colors__color__icontains=rgb_part).distinct()
            except ValueError:
                # Invalid hex color - return empty queryset
                return queryset.none()
        else:
            # Invalid length - return empty queryset
            return queryset.none()

    def filter_rating(self, queryset, name, value):
        """Filter by minimum average rating"""
        if not value:
            return queryset
        
        try:
            min_rating_value = float(value)
            # Annotate with average rating and filter
            return queryset.annotate(
                avg_rating=Avg('comments__review_rating')
            ).filter(avg_rating__gte=min_rating_value)
        except (ValueError, TypeError):
            return queryset

    def filter_has_discount(self, queryset, name, value):
        """Filter products that have discount price"""
        if value is True:
            return queryset.filter(discount_price__gt=0, discount_price__isnull=False)
        elif value is False:
            return queryset.filter(Q(discount_price__isnull=True) | Q(discount_price=0))
        return queryset 