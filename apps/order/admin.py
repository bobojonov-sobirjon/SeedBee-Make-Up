from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import CardDetails, Order
from apps.market.models import Product


@admin.register(CardDetails)
class CardDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'card_holder', 'card_number_masked', 'expiration_date', 'created_at', 'is_expired')
    list_filter = ('expiration_date', 'created_at', 'user')
    search_fields = ('user__email', 'card_holder', 'card_number')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Пользователь'), {
            'fields': ('user',)
        }),
        (_('Информация о карте'), {
            'fields': ('card_number', 'card_holder', 'expiration_date')
        }),
        (_('Системная информация'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email if obj.user else _('Неизвестный пользователь')
    user_email.short_description = _('Email пользователя')
    user_email.admin_order_field = 'user__email'
    
    def card_number_masked(self, obj):
        if obj.card_number and len(obj.card_number) >= 4:
            return f"**** **** **** {obj.card_number[-4:]}"
        return "**** **** **** ****"
    card_number_masked.short_description = _('Номер карты')
    
    def is_expired(self, obj):
        if not obj.expiration_date or len(obj.expiration_date) != 4:
            return format_html('<span style="color: red;">{}</span>', _('Неверный формат'))
        month = int(obj.expiration_date[:2])
        year = int(obj.expiration_date[2:])
        current_year = timezone.now().year % 100
        current_month = timezone.now().month
        if year < current_year or (year == current_year and month < current_month):
            return format_html('<span style="color: red;">{}</span>', _('Истекла'))
        return format_html('<span style="color: green;">{}</span>', _('Активна'))
    is_expired.short_description = _('Статус карты')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_email', 'full_name', 'phone', 'address', 'total_price', 'products_count', 'created_at', 'status_display', 'payment_status_display')
    list_filter = ('created_at', 'user', 'total_price', 'payment_status')
    search_fields = ('order_id', 'user__email')
    readonly_fields = ('order_id', 'created_at', 'products_display')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('order_id', 'user', 'full_name', 'phone', 'address', 'total_price', 'payment_status')
        }),
        (_('Продукты'), {
            'fields': ('products_display',),
            'classes': ('collapse',)
        }),
        (_('Системная информация'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email if obj.user else _('Неизвестный пользователь')
    user_email.short_description = _('Email пользователя')
    user_email.admin_order_field = 'user__email'
    
    def products_count(self, obj):
        if obj.products:
            return len(obj.products)
        return 0
    products_count.short_description = _('Количество продуктов')
    
    def products_display(self, obj):
        if not obj.products:
            return _('Нет продуктов')
        
        html = '<ul>'
        for product in obj.products:
            product_id = product.get('id', 'N/A')
            product_name = product.get('name', 'Неизвестный продукт')
            quantity = product.get('quantity', 1)
            price = product.get('price', 0)
            try:
                prod = Product.objects.get(id=product_id)
                thumbnail = prod.thumbnail.url if prod.thumbnail else ''
                image_html = f'<img src="{thumbnail}" style="max-width:50px; max-height:50px;" alt="{product_name}">' if thumbnail else ''
            except Product.DoesNotExist:
                image_html = ''
            
            html += f'<li>{image_html} <strong>{product_name}</strong> (ID: {product_id}) - '
            html += f'Количество: {quantity}, Цена: {price} ₽</li>'
        html += '</ul>'
        
        return format_html(html)
    products_display.short_description = _('Детали продуктов')
    
    def status_display(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        # Simple status logic based on creation time
        now = timezone.now()
        if obj.created_at > now - timedelta(hours=1):
            return format_html('<span style="color: blue;">{}</span>', _('Новый'))
        elif obj.created_at > now - timedelta(days=1):
            return format_html('<span style="color: orange;">{}</span>', _('В обработке'))
        else:
            return format_html('<span style="color: green;">{}</span>', _('Завершен'))
    status_display.short_description = _('Статус заказа')

    def payment_status_display(self, obj):
        return obj.get_payment_status_display()
    payment_status_display.short_description = _('Статус оплаты')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        # Orders should be created through the application, not admin
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of orders
        return False

