from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from djoser.conf import settings
from rest_framework.settings import api_settings

User = get_user_model()



class CitizenUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)
    middle_name = serializers.CharField(max_length=255, write_only=True)
    contact_number = serializers.IntegerField(write_only=True)
    birthdate = serializers.DateField(write_only=True)
    gender = serializers.CharField(max_length=6, write_only=True)
    citizenship = serializers.CharField(max_length=255, write_only=True)
    civil_status = serializers.CharField(max_length=255, write_only=True)
    placeofbirth = serializers.CharField(max_length=255, write_only=True)
    address = serializers.CharField(max_length=255, write_only=True)
    highesteducationattainment = serializers.CharField(max_length=255, write_only=True)
    occupation = serializers.CharField(max_length=255, write_only=True)
    Valid_ID = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
            "first_name",
            "last_name",
            "middle_name",
            "contact_number",
            "birthdate",
            "gender",
            "citizenship",
            "civil_status",
            "placeofbirth",
            "address",
            "highesteducationattainment",
            "occupation",
            "Valid_ID",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs
    
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user