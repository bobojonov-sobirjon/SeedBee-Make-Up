from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from apps.market.models import (
	TopLevelCategory, SubCategory, Category, Product, ProductImage,
	ProductColor, CommentAndReviewProduct
)
from apps.market.serializers import (
	TopLevelCategorySerializer, ProductSerializer,
	CommentAndReviewProductCreateSerializer
)
from apps.market.filters import ProductFilter


class ProductPagination(PageNumberPagination):
	page_size = 12
	page_size_query_param = 'page_size'
	max_page_size = 100


class TopLevelCategoryListView(APIView):
	permission_classes = [AllowAny]
	"""
	View to list all top-level categories.
	"""
	@swagger_auto_schema(
		operation_id='list_top_level_categories',
		operation_description='Retrieve a list of all top-level categories.',
		operation_summary='List Top-Level Categories',
		tags=['Categories'],
		responses={
			200: TopLevelCategorySerializer(many=True, read_only=True),
			400: 'Bad Request'
		}
	)
	def get(self, request):
		categories = TopLevelCategory.objects.all()
		serializer = TopLevelCategorySerializer(categories, many=True, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListView(APIView):
	permission_classes = [AllowAny]
	filter_backends = [DjangoFilterBackend]
	filterset_class = ProductFilter
	
	"""
	Enhanced view to list products with pagination, search, and filtering using Django Filter.
	"""
	@swagger_auto_schema(
		operation_id='list_products',
		operation_description='Retrieve a paginated list of products with search and filtering capabilities.',
		operation_summary='List Products with Filters',
		tags=['Products'],
		manual_parameters=[
			openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
			openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page (max 100)", type=openapi.TYPE_INTEGER),
			openapi.Parameter('search', openapi.IN_QUERY, description="Search by product name in any language", type=openapi.TYPE_STRING),
			openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER),
			openapi.Parameter('brand', openapi.IN_QUERY, description="Filter by brand name", type=openapi.TYPE_STRING),
			openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price filter", type=openapi.TYPE_NUMBER),
			openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price filter", type=openapi.TYPE_NUMBER),
			openapi.Parameter('color', openapi.IN_QUERY, description="Filter by color hex code (e.g., #FF0000)", type=openapi.TYPE_STRING),
			openapi.Parameter('min_rating', openapi.IN_QUERY, description="Minimum average rating filter (0-5)", type=openapi.TYPE_NUMBER),
			openapi.Parameter('has_discount', openapi.IN_QUERY, description="Filter products with discount (true/false)", type=openapi.TYPE_BOOLEAN),
			openapi.Parameter('is_popular', openapi.IN_QUERY, description="Filter popular products (true/false)", type=openapi.TYPE_BOOLEAN),
			openapi.Parameter('is_new', openapi.IN_QUERY, description="Filter new products (true/false)", type=openapi.TYPE_BOOLEAN),
			openapi.Parameter('is_discounted', openapi.IN_QUERY, description="Filter products with discount price (true/false)", type=openapi.TYPE_BOOLEAN),
			openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by: created_at, -created_at, price, -price, id, -id", type=openapi.TYPE_STRING),
		],
		responses={
			200: openapi.Response(
				description='Paginated list of products',
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of products'),
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
		# Get all products
		queryset = Product.objects.all()
		
		# Apply filters using Django Filter
		filterset = ProductFilter(request.query_params, queryset=queryset)
		filtered_queryset = filterset.qs
		
		# Apply pagination
		paginator = ProductPagination()
		paginated_products = paginator.paginate_queryset(filtered_queryset, request)
		
		# Serialize the data
		serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
		
		# Return paginated response
		return paginator.get_paginated_response(serializer.data)


class ProductDetailView(APIView):
	permission_classes = [AllowAny]

	@swagger_auto_schema(
		operation_id='get_product_detail',
		operation_description='Retrieve detailed information about a specific product by its ID.',
		operation_summary='Get Product Detail',
		tags=['Products'],
		responses={
			200: ProductSerializer,
			404: 'Product not found'
		}
	)
	def get(self, request, pk):
		try:
			product = Product.objects.get(pk=pk)
			serializer = ProductSerializer(product, context={'request': request})
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Product.DoesNotExist:
			return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentAndReviewCreateView(APIView):
	permission_classes = [AllowAny]

	@swagger_auto_schema(
		request_body=CommentAndReviewProductCreateSerializer,
		tags=['Products'],
		operation_id='create_product_review',
		operation_description='Create a new comment or review for a product.',
		operation_summary='Create Product Review',
		responses={
			201: CommentAndReviewProductCreateSerializer,
			400: 'Bad Request'
		}
	)
	def post(self, request):
		serializer = CommentAndReviewProductCreateSerializer(
			data=request.data, 
			context={'request': request, 'view': self}
		)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)