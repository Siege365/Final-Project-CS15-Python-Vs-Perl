"""
ShopPy - Product Model
Handles product catalog management.
Equivalent to Perl ECommerce::Models::Product
"""

from django.db import models
from django.utils import timezone


class Product(models.Model):
    """
    Product model for ShopPy e-commerce system.
    Mirrors the Perl products table structure.
    """

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Home', 'Home'),
        ('Sports', 'Sports'),
        ('Toys', 'Toys'),
        ('Food', 'Food'),
        ('Beauty', 'Beauty'),
        ('Automotive', 'Automotive'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    image_url = models.URLField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        """Check if product is low on stock."""
        return self.stock_quantity <= self.reorder_level and self.stock_quantity > 0

    @property
    def is_out_of_stock(self):
        """Check if product is out of stock."""
        return self.stock_quantity <= 0

    @property
    def stock_status(self):
        """Return stock status as string."""
        if not self.is_active:
            return 'discontinued'
        elif self.is_out_of_stock:
            return 'out_of_stock'
        elif self.is_low_stock:
            return 'low_stock'
        return 'in_stock'

    def update_stock(self, quantity_change, transaction_type, reference_id=None, notes=''):
        """
        Update product stock and record transaction.
        Positive quantity_change increases stock, negative decreases.
        """
        from lib.ECommerce.Models.Order import InventoryTransaction

        self.stock_quantity += quantity_change
        self.save()

        # Record the transaction
        InventoryTransaction.objects.create(
            product=self,
            quantity_change=quantity_change,
            transaction_type=transaction_type,
            reference_id=reference_id,
            notes=notes
        )

        return True

    @classmethod
    def get_active_products(cls):
        """Get all active products."""
        return cls.objects.filter(is_active=True).order_by('id')

    @classmethod
    def get_low_stock_products(cls):
        """Get products with low stock levels."""
        return cls.objects.filter(
            is_active=True,
            stock_quantity__lte=models.F('reorder_level')
        ).order_by('stock_quantity')

    @classmethod
    def search_products(cls, search_term, active_only=True):
        """Search products by name, SKU, or description."""
        from django.db.models import Q
        queryset = cls.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.filter(
            Q(name__icontains=search_term) |
            Q(sku__icontains=search_term) |
            Q(description__icontains=search_term)
        ).order_by('id')

    @classmethod
    def get_products_by_category(cls, category, active_only=True):
        """Get products by category."""
        queryset = cls.objects.filter(category=category)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('id')

    @classmethod
    def get_categories(cls):
        """Get list of all category choices."""
        return [cat[0] for cat in cls.CATEGORY_CHOICES]
