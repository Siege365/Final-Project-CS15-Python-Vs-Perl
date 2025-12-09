"""
ShopPy - User Model
Handles user authentication and management.
Equivalent to Perl ECommerce::Models::User
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for ShopPy users."""

    def create_user(self, username, email, password=None, role='customer', **extra_fields):
        """Create and save a regular user."""
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, email, password, role='admin', **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for ShopPy e-commerce system.
    Mirrors the Perl users table structure.
    """

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for Django admin
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Check if user is admin."""
        return self.role == 'admin'

    @property
    def is_staff_member(self):
        """Check if user is staff or admin."""
        return self.role in ['staff', 'admin']

    @property
    def is_customer(self):
        """Check if user is customer."""
        return self.role == 'customer'

    def get_customer_profile(self):
        """Get associated customer profile if exists."""
        try:
            return self.customer_profile
        except:
            return None
