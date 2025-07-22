from rest_framework import serializers
from django.utils import timezone
from datetime import date

from apps.order.models import CardDetails, Order
from apps.market.models import Product
from apps.market.serializers import ProductSerializer


class CardDetailsSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(max_length=19)  # Allow spaces in input
    expiration_date = serializers.CharField(max_length=4)

    class Meta:
        model = CardDetails
        fields = ['id', 'user', 'card_number', 'card_holder', 'expiration_date', 'created_at', 'payme_token', 'verified']
        read_only_fields = ['id', 'user', 'created_at', 'payme_token', 'verified']
        
    def validate_card_number(self, value):
        """Validate card number format and Luhn algorithm"""
        # Remove spaces and check length
        card_number = value.replace(' ', '')
        
        if len(card_number) != 16:
            raise serializers.ValidationError("Номер карты должен состоять из 16 цифр.")
        
        if not card_number.isdigit():
            raise serializers.ValidationError("Номер карты должен состоять только из цифр.")
        
        # Basic Luhn algorithm check
        if not self._luhn_check(card_number):
            raise serializers.ValidationError("Неверный номер карты.")
        
        return card_number
    
    def validate_expiration_date(self, value):
        """Validate expiration date in MMYY format"""
        if len(value) != 4 or not value.isdigit():
            raise serializers.ValidationError("Формат даты истечения: MMYY (например, 0325 для марта 2025)")
        month = int(value[:2])
        year = int(value[2:])
        if month < 1 or month > 12:
            raise serializers.ValidationError("Неверный месяц (01-12)")
        current_year = date.today().year % 100
        current_month = date.today().month
        if year < current_year or (year == current_year and month < current_month):
            raise serializers.ValidationError("Дата истечения срока действия карты должна быть в будущем.")
        return value
    
    def validate_card_holder(self, value):
        """Validate card holder name"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Имя держателя карты должно содержать минимум 2 символа.")
        return value.strip()
    
    def _luhn_check(self, card_number):
        """Luhn algorithm for card number validation"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0
        
    def create(self, validated_data):
        """Create card details with current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_id', 'user', 'created_at', 'payment_status')

    def get_products(self, obj):
        product_ids = [p['id'] for p in obj.products]
        products = Product.objects.filter(id__in=product_ids)
        return ProductSerializer(products, many=True, context=self.context).data