from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.banner.models import Banner, Partner, Advertisement, Blog
from apps.banner.serializers import (
	BannerSerializer, PartnerSerializer, AdvertisementSerializer, BlogSerializer
)


class BannerListView(APIView):
	permission_classes = [AllowAny]
	pagination_class = PageNumberPagination

	@swagger_auto_schema(
		operation_id='list_banners',
		operation_description='Retrieve a list of all banners.',
		operation_summary='List Banners',
		tags=['Banners'],
		responses={
			200: BannerSerializer(many=True, read_only=True),
			400: 'Bad Request'
		}
	)
	def get(self, request):
		banners = Banner.objects.all()
		paginator = self.pagination_class()
		page = paginator.paginate_queryset(banners, request)
		if page is not None:
			serializer = BannerSerializer(page, many=True, context={'request': request})
			return paginator.get_paginated_response(serializer.data)

		serializer = BannerSerializer(banners, many=True, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)


class PartnerListView(APIView):
	permission_classes = [AllowAny]
	pagination_class = PageNumberPagination

	@swagger_auto_schema(
		operation_id='list_partners',
		operation_description='Retrieve a list of all partners.',
		operation_summary='List Partners',
		tags=['Partners'],
		responses={
			200: PartnerSerializer(many=True, read_only=True),
			400: 'Bad Request'
		}
	)
	def get(self, request):
		partners = Partner.objects.all()
		paginator = self.pagination_class()
		page = paginator.paginate_queryset(partners, request)
		if page is not None:
			serializer = PartnerSerializer(page, many=True, context={'request': request})
			return paginator.get_paginated_response(serializer.data)

		serializer = PartnerSerializer(partners, many=True, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementListView(APIView):
	permission_classes = [AllowAny]
	pagination_class = PageNumberPagination

	@swagger_auto_schema(
		operation_id='list_advertisements',
		operation_description='Retrieve a list of all advertisements.',
		operation_summary='List Advertisements',
		tags=['Advertisements'],
		responses={
			200: AdvertisementSerializer(many=True, read_only=True),
			400: 'Bad Request'
		}
	)
	def get(self, request):
		advertisements = Advertisement.objects.all()
		paginator = self.pagination_class()
		page = paginator.paginate_queryset(advertisements, request)
		if page is not None:
			serializer = AdvertisementSerializer(page, many=True, context={'request': request})
			return paginator.get_paginated_response(serializer.data)
		serializer = AdvertisementSerializer(advertisements, many=True, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)


class BlogListView(APIView):
	permission_classes = [AllowAny]
	pagination_class = PageNumberPagination

	@swagger_auto_schema(
		operation_id='list_blogs',
		operation_description='Retrieve a list of all blogs.',
		operation_summary='List Blogs',
		tags=['Blogs'],
		responses={
			200: BlogSerializer(many=True, read_only=True),
			400: 'Bad Request'
		}
	)
	def get(self, request):
		blogs = Blog.objects.all()
		paginator = self.pagination_class()
		page = paginator.paginate_queryset(blogs, request)
		if page is not None:
			serializer = BlogSerializer(page, many=True, context={'request': request})
			return paginator.get_paginated_response(serializer.data)
		serializer = BlogSerializer(blogs, many=True, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)
