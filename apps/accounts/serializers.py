from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

User = get_user_model()


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'placeholder': 'Enter password'})
    password_confirm = serializers.CharField(write_only=True, required=False,
                                             style={'placeholder': 'Enter password confirmation'})

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name',
                  'password', 'password_confirm', 'is_agree']

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # If password is provided, password_confirm must also be provided and match
        if password or password_confirm:
            if not password:
                raise ValidationError({"password": "Password is required when password_confirm is provided"})
            if not password_confirm:
                raise ValidationError({"password_confirm": "Password confirmation is required when password is provided"})
            if password != password_confirm:
                raise ValidationError({"password_confirm": "Passwords do not match"})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        if not password:
            raise ValidationError({"password": "Password is required for user creation"})

        email = validated_data.pop('email')
        
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            **validated_data
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        try:
            instance.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        instance.save()
        return instance


class CustomAuthTokenSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'placeholder': 'Enter password'})

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Телефон и пароль, оба поля обязательны")

        user_model = get_user_model()

        user = user_model.objects.filter(email=identifier).first()

        if user is None:
            raise AuthenticationFailed("Неверные данные, пользователь не найден")

        if not user.check_password(password):
            raise AuthenticationFailed("Неверные данные, неправильный пароль")

        return {
            'user': user,
        }


class CustomUserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'email', 'first_name', 'last_name', 'avatar',
        ]

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
