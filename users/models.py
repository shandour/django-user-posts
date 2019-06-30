import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import URLValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if email is None:
            raise TypeError('Users must have an email address.')
        # may be changed if social login is added
        if password is None:
            raise TypeError('Users must have a password.')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password, is_superuser=True)

        return user


class Company(models.Model):
    name = models.CharField(max_length=100)
    legal_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    site = models.CharField(max_length=100, validators=[URLValidator])


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    time_zone = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        related_name='users',
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f'{str(self.pk)}; {self.email}'
