from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Company
from .utils import check_email, handle_nested_company_object


User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'legal_name',
            'location',
            'description',
            'site',
        )


class UserSerializer(
    serializers.ModelSerializer,
):
    company = CompanySerializer(required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'company',
            'location',
        )

    # an explicit update method for handling nested fields
    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)
        user = super().update(instance, validated_data)
        handle_nested_company_object(user, company_data)

        return user


class RegistrationSerializer(
        serializers.ModelSerializer,
):
    company = CompanySerializer(required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'company',
            'location',
            'password',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')

        return data

    def validate_email(self, value):
        success, site_down = check_email(value)

        if site_down:
            raise serializers.ValidationError(
                _('Email verification site is down. Please try again later.')
            )

        if success:
            return value
        else:
            raise serializers.ValidationError(
                _('Email deemed inappropriate. '
                  'Possible reasons: looks like a random string, '
                  'is malformed, reliability score too low.')
            )

    # an explicit create method for handling nested fields
    def create(self, validated_data):
        company_data = validated_data.pop('company', None)
        user = super().create(validated_data)
        handle_nested_company_object(user, company_data)

        return user

