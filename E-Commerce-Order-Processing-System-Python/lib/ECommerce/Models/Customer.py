"""
ShopPy - Customer Model
Handles customer profile data.
Equivalent to Perl ECommerce::Models::Customer
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Customer(models.Model):
    """
    Customer profile model for ShopPy e-commerce system.
    Mirrors the Perl customers table structure.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    zip_code = models.CharField(max_length=20, blank=True, default='')
    country = models.CharField(max_length=100, default='USA')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """Return customer's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def full_address(self):
        """Return formatted full address."""
        parts = [self.address]
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.zip_code:
            parts.append(self.zip_code)
        if self.country:
            parts.append(self.country)
        return ', '.join(filter(None, parts))

    @classmethod
    def get_customer_by_user_id(cls, user_id):
        """Get customer by associated user ID."""
        try:
            return cls.objects.get(user_id=user_id)
        except cls.DoesNotExist:
            return None

    def get_order_count(self):
        """Get total number of orders for this customer."""
        return self.orders.count()

    def get_total_spent(self):
        """Get total amount spent by this customer."""
        from django.db.models import Sum
        result = self.orders.exclude(status='cancelled').aggregate(total=Sum('total'))
        return result['total'] or 0

    @classmethod
    def search_customers(cls, search_term):
        """Search customers by name, phone, or email."""
        from django.db.models import Q
        return cls.objects.select_related('user').filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(phone__icontains=search_term) |
            Q(user__email__icontains=search_term)
        ).order_by('-created_at')
