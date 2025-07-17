from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings

from urllib.parse import urlparse, parse_qs

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

from apps.accounts.serializers import (
	SignUpSerializer, CustomAuthTokenSerializer, CustomUserDetailSerializer,
	PasswordUpdateSerializer,
)

User = get_user_model()


class UserSignupView(APIView):
	permission_classes = [AllowAny]

	@swagger_auto_schema(request_body=SignUpSerializer, tags=['Account'])
	def post(self, request, *args, **kwargs):
		serializer = SignUpSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenView(APIView):
	permission_classes = [AllowAny]

	@swagger_auto_schema(request_body=CustomAuthTokenSerializer, tags=['Account'])
	def post(self, request):
		serializer = CustomAuthTokenSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.validated_data['user']
			refresh = RefreshToken.for_user(user)

			return Response({
				'refresh': str(refresh),
				'access': str(refresh.access_token),
			}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailView(APIView):
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		responses={200: CustomUserDetailSerializer()},
		operation_description="Retrieve details of the authenticated user.", tags=['Account']
	)
	def get(self, request):
		user = request.user
		serializer = CustomUserDetailSerializer(user, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		responses={200: CustomUserDetailSerializer()},
		request_body=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'first_name': openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
				'last_name': openapi.Schema(type=openapi.TYPE_STRING, max_length=30),
				'avatar': openapi.Schema(type=openapi.TYPE_FILE, description='User avatar image'),
			}
		),
		operation_description="Update the authenticated user's profile. Supports both JSON and multipart/form-data for avatar uploads.",
		tags=['Account']
	)
	def put(self, request):
		user = request.user
		serializer = CustomUserDetailSerializer(user, data=request.data, partial=True, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		responses={204: 'No Content'},
		operation_description="Delete the authenticated user's account.", tags=['Account']
	)
	def delete(self, request):
		user = request.user
		user.delete()
		return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CustomUserView(APIView):
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		responses={200: CustomUserDetailSerializer()},
		operation_description="Retrieve details of the guest user.", tags=['Account']
	)
	def get(self, request, *args, **kwargs):
		user_model = get_user_model()
		user = get_object_or_404(user_model, id=kwargs.get('id'))
		serializer = CustomUserDetailSerializer(user, context={'request': request})
		return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordUpdateView(APIView):
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		request_body=PasswordUpdateSerializer,
		tags=['Account'],
		responses={
			200: "Password updated successfully.",
			400: "Bad Request: Password update failed."
		},
		operation_description="Update the authenticated user's password."
	)
	def patch(self, request):
		serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.update(request.user, serializer.validated_data)
			return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
