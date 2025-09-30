from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if password and len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class customUser(AbstractUser):
    username = None  # removes username
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=14, default=None, blank=True, null=True)
    account_creation_date = models.DateTimeField(auto_now_add=True)  # stores full date + time

    USERNAME_FIELD = 'email'  # use email as login
    REQUIRED_FIELDS = ['first_name',
                       'last_name']  # mandatory fields on creation # fields required when creating superuser

    objects = CustomUserManager()  # use custom manager

    def __str__(self):
        return self.email

