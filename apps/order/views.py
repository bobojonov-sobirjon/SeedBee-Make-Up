from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
import requests
import json
import uuid
from apps.market.models import Product

from apps.order.models import CardDetails, Order
from apps.order.serializers import CardDetailsSerializer
from apps.order.serializers import OrderSerializer

import logging
from django.conf import settings
from django.db import transaction
from requests.exceptions import RequestException

logger = logging.getLogger(__name__);

class PaymeClient:
    def __init__(self):
        self.url = settings.PAYME_URL;
        self.id = settings.PAYME_ID;
        self.key = settings.PAYME_KEY;
        self.headers = {
            "X-Auth": f"{self.id}:{self.key}",
            "Content-Type": "application/json",
        };
        self.timeout = 10  # Added for performance

    def _make_request(self, payload):
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=self.timeout);
            response.raise_for_status();
            return response.json();
        except RequestException as e:
            logger.error(f"Payme request failed: {str(e)}");
            raise;

    def create_card(self, card_number, expire):
        payload = {
            "id": 123,
            "method": "cards.create",
            "params": {"card": {"number": card_number, "expire": expire}, "save": True}
        };
        return self._make_request(payload);

    def get_verify_code(self, token):
        payload = {"id": 123, "method": "cards.get_verify_code", "params": {"token": token}};
        return self._make_request(payload);

    def verify_card(self, token, code):
        payload = {"id": 123, "method": "cards.verify", "params": {"token": token, "code": code}};
        return self._make_request(payload);

    def create_receipt(self, amount, order_id, items):
        payload = {
            "id": 123,
            "method": "receipts.create",
            "params": {
                "amount": amount,
                "account": {"order_id": order_id},
                "detail": {"receipt_type": 0, "items": items}
            }
        };
        return self._make_request(payload);

    def pay_receipt(self, receipt_id, token):
        payload = {"id": 123, "method": "receipts.pay", "params": {"id": receipt_id, "token": token}};
        return self._make_request(payload);

class CardDetailsView(APIView):
    permission_classes = [IsAuthenticated]
 
    @swagger_auto_schema(
        request_body=CardDetailsSerializer,
        tags=['Card Details'],
        operation_id='create_card_details',
        operation_description='Create a new card details for the authenticated user',
        operation_summary='Create Card Details',
        responses={
            201: CardDetailsSerializer,
            400: 'Bad Request',
            409: 'Card already exists'
        }
    )
    def post(self, request):
        """Create new card details for the authenticated user"""
        try:
            card_number = request.data.get('card_number', '').replace(' ', '')
            existing_card = CardDetails.objects.filter(
                user=request.user, 
                card_number=card_number
            ).first()
            
            if existing_card:
                return Response(
                    {'error': 'Карта с таким номером уже существует'}, 
                    status=status.HTTP_409_CONFLICT
                )
            
            serializer = CardDetailsSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                card = serializer.save()
                # Payme integration
                payme_client = PaymeClient()
                try:
                    data = payme_client.create_card(card.card_number, card.expiration_date)
                    if 'result' in data and 'card' in data['result']:
                        card.payme_token = data['result']['card']['token']
                        card.save()
                except RequestException:
                    logger.warning("Payme card creation failed, proceeding without token")
                serializer = CardDetailsSerializer(card, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error creating card: {str(e)}")
            return Response(
                {'error': 'Ошибка при создании карты'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CardVerifyCodeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'card_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['card_id']
        ),
        tags=['Card Details'],
        operation_id='card_verify_code',
        operation_description='Send verification code for the card.',
        operation_summary='Get Card Verify Code',
        responses={
            200: 'Success',
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def post(self, request):
        card_id = request.data.get('card_id')
        card = get_object_or_404(CardDetails, id=card_id, user=request.user)
        if not card.payme_token:
            return Response({"error": "Карта не создана в Payme"}, status=400)
        payme_client = PaymeClient()
        try:
            data = payme_client.get_verify_code(card.payme_token)
            return Response(data, status=200)
        except RequestException as e:
            return Response({"error": str(e)}, status=400)

class CardVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'card_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'code': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['card_id', 'code']
        ),
        tags=['Card Details'],
        operation_id='card_verify',
        operation_description='Verify the card with SMS code.',
        operation_summary='Verify Card',
        responses={
            200: 'Success',
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    def post(self, request):
        card_id = request.data.get('card_id')
        code = request.data.get('code')
        if not code:
            return Response({"error": "Требуется код"}, status=400)
        card = get_object_or_404(CardDetails, id=card_id, user=request.user)
        if not card.payme_token:
            return Response({"error": "Карта не создана в Payme"}, status=400)
        payme_client = PaymeClient()
        try:
            data = payme_client.verify_card(card.payme_token, code)
            if 'result' in data and 'card' in data['result']:
                card.payme_token = data['result']['card']['token']
                card.verified = True
                card.save()
                return Response({"success": True, "data": data}, status=200)
            else:
                return Response({"error": "Проверка не удалась"}, status=400)
        except RequestException as e:
            return Response({"error": str(e)}, status=400)

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_list': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    )
                ),
                'card_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['product_list', 'card_id']
        ),
        tags=['Orders'],
        operation_id='create_order',
        operation_description='Create and pay for an order using Payme.',
        operation_summary='Create Order',
        responses={
            200: OrderSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        product_list = request.data.get('product_list', [])
        card_id = request.data.get('card_id')
        address = request.data.get('address')
        phone = request.data.get('phone')
        full_name = request.data.get('full_name')
        if not product_list or not card_id:
            return Response({"error": "Требуются product_list и card_id"}, status=400)

        card = get_object_or_404(CardDetails, id=card_id, user=request.user, verified=True)
        products = self._validate_products(product_list)

        items, total_amount, products_json = self._prepare_order_data(products, product_list)

        with transaction.atomic():
            order = self._create_and_pay_order(card, total_amount, items, products_json, address, phone, full_name)
            if order.payment_status == 4:
                self._update_stock(products, product_list)
            status_desc = dict(Order.PAYMENT_STATES).get(order.payment_status, "Неизвестное состояние")
            return Response({
                "success": order.payment_status == 4,
                "state": order.payment_status,
                "status": status_desc,
                "order_id": order.order_id,
            }, status=200)

    def _validate_products(self, product_list):
        product_ids = [p['product_id'] for p in product_list]
        products = Product.objects.filter(id__in=product_ids)
        if len(products) != len(product_ids):
            raise ValueError("Некоторые продукты не найдены")
        for prod in products:
            for pl in product_list:
                if pl['product_id'] == prod.id and prod.stock < pl['quantity']:
                    raise ValueError(f"Недостаточно запасов для продукта {prod.id}")
        return products

    def _prepare_order_data(self, products, product_list):
        items = []
        total_amount = 0.0
        products_json = []
        for prod in products:
            for pl in product_list:
                if pl['product_id'] == prod.id:
                    quantity = pl['quantity']
                    price = prod.discount_price if prod.discount_price else prod.price
                    item_total = price * quantity
                    discount = (prod.price - price) * quantity if prod.discount_price else 0
                    total_amount += item_total
                    items.append({
                        "title": prod.safe_translation_getter('name', any_language=True),
                        "price": int(price * 100),
                        "count": quantity,
                        "code": prod.code,
                        "package_code": prod.package_code,
                        "vat_percent": 0,
                        "discount": int(discount * 100),
                    })
                    products_json.append({
                        "id": prod.id,
                        "name": prod.safe_translation_getter('name', any_language=True),
                        "quantity": quantity,
                        "price": price
                    })
        return items, int(total_amount * 100), products_json

    def _create_and_pay_order(self, card, total_amount, items, products_json, address=None, phone=None, full_name=None):
        order_uuid = uuid.uuid4()
        order_id = str(order_uuid)
        payme_client = PaymeClient()
        data = payme_client.create_receipt(total_amount, order_id, items)
        receipt_id = data.get('result', {}).get('receipt', {}).get('_id')
        if not receipt_id:
            raise ValueError("Неверный ответ от Payme")

        pay_data = payme_client.pay_receipt(receipt_id, card.payme_token)
        state = pay_data.get('result', {}).get('receipt', {}).get('state')
        if not state:
            raise ValueError("Неверный ответ оплаты от Payme")

        order = Order.objects.create(
            user=self.request.user,
            order_id=order_uuid,
            products=products_json,
            total_price=total_amount / 100,
            payment_status=state,
            address=address,
            phone=phone,
            full_name=full_name
        )
        return order

    def _update_stock(self, products, product_list):
        for prod in products:
            for pl in product_list:
                if pl['product_id'] == prod.id:
                    prod.stock -= pl['quantity']
                    prod.save()

    
class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='list_user_orders',
        operation_description='Retrieve a paginated list of all orders for the authenticated user.',
        operation_summary='List User Orders',
        tags=['Orders'],
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page (max 50)", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description='Paginated list of user orders',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of orders'),
                        'next': openapi.Schema(type=openapi.TYPE_STRING, description='Next page URL'),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, description='Previous page URL'),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY, 
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        ),
                    }
                )
            ),
            400: 'Bad Request'
        }
    )
    def get(self, request):
        # Get all orders for the authenticated user
        queryset = Order.objects.filter(user=request.user).order_by('-created_at')
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = 'page_size'
        paginator.max_page_size = 50
        
        paginated_orders = paginator.paginate_queryset(queryset, request)
        
        # Serialize the data
        serializer = OrderSerializer(paginated_orders, many=True, context={'request': request})
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
	
