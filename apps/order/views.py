from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from apps.order.models import CardDetails, Order
from apps.order.serializers import CardDetailsSerializer


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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {'error': 'Ошибка при создании карты'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
	
	
