from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
            'domain',
        )


class UserSerializer(
    serializers.ModelSerializer,
):
    company = CompanySerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'company',
            'location',
        )

    def to_internal_value(self, data):
        company = data.get('company')
        user = self.instance
        if company:
            if user.company:
                if not company.get('id'):
                    raise serializers.ValidationError(
                        {'company': _('No company id provided')})
                elif company.get('id') != user.company.pk:
                    raise serializers.ValidationError(
                        {'company': _('Incorrect company id. '
                                      f'Should be {user.company.pk}')
                        })

        return super().to_internal_value(data)

    # an explicit update method for handling nested fields
    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)
        user = super().update(instance, validated_data)

        if company_data and user.company and not company_data.get('id'):
            company_data['id'] = user.company.pk

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
        data['id'] = instance.pk
        refresh = RefreshToken.for_user(instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

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
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        handle_nested_company_object(user, company_data)

        return user


class CustomizedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        data = super().validate(data)
        data['user'] = UserSerializer(self.user).data

        return data
