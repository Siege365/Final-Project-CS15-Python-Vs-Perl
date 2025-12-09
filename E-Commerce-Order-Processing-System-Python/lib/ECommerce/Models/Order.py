"""
ShopPy - Order Model
Handles order processing and management.
Equivalent to Perl ECommerce::Models::Order
"""

from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
import random
from datetime import datetime


class Order(models.Model):
    """
    Order model for ShopPy e-commerce system.
    Mirrors the Perl orders table structure.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        default=''
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    shipping_address = models.TextField(blank=True, default='')
    billing_address = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        date_str = datetime.now().strftime('%Y%m%d')
        random_num = random.randint(10000, 99999)
        return f"ORD-{date_str}-{random_num}"

    @classmethod
    def create_from_cart(cls, customer, cart_items, payment_method, shipping_address, billing_address=None, notes=''):
        """
        Create order from shopping cart.
        cart_items should be list of dicts with product_id, quantity, price, name
        """
        from lib.ECommerce.Models.Product import Product
        from lib.ECommerce.Config import APP_CONFIG

        if not cart_items:
            return {'success': False, 'message': 'Cart is empty'}

        subtotal = 0
        order_items_data = []

        # Validate cart and calculate totals
        for item in cart_items:
            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                return {'success': False, 'message': f"Product not found: {item.get('name', 'Unknown')}"}

            if product.stock_quantity < item['quantity']:
                return {'success': False, 'message': f"Insufficient stock for: {product.name}"}

            item_subtotal = float(product.price) * item['quantity']
            subtotal += item_subtotal

            order_items_data.append({
                'product': product,
                'product_name': product.name,
                'product_sku': product.sku,
                'quantity': item['quantity'],
                'unit_price': product.price,
                'subtotal': item_subtotal,
            })

        # Calculate tax and shipping
        tax_rate = APP_CONFIG.get('tax_rate', 0.08)
        shipping_rate = APP_CONFIG.get('shipping_rate', 5.00)
        free_shipping_threshold = APP_CONFIG.get('free_shipping_threshold', 100.00)

        tax = subtotal * tax_rate
        shipping = 0 if subtotal >= free_shipping_threshold else shipping_rate
        total = subtotal + tax + shipping

        try:
            with transaction.atomic():
                # Create order
                order = cls.objects.create(
                    order_number=cls.generate_order_number(),
                    customer=customer,
                    subtotal=subtotal,
                    tax=tax,
                    shipping=shipping,
                    total=total,
                    payment_method=payment_method,
                    shipping_address=shipping_address,
                    billing_address=billing_address or shipping_address,
                    notes=notes
                )

                # Create order items and update stock
                for item_data in order_items_data:
                    product = item_data.pop('product')
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        **item_data
                    )

                    # Update stock
                    product.update_stock(
                        quantity_change=-item_data['quantity'],
                        transaction_type='sale',
                        reference_id=order.id,
                        notes=f"Order {order.order_number}"
                    )

                return {
                    'success': True,
                    'order_id': order.id,
                    'order_number': order.order_number
                }

        except Exception as e:
            return {'success': False, 'message': f"Failed to create order: {str(e)}"}

    def update_status(self, new_status):
        """Update order status."""
        self.status = new_status
        self.save()
        return {'success': True}

    def cancel_order(self):
        """Cancel order and restore stock."""
        if self.status not in ['pending', 'processing']:
            return {'success': False, 'message': 'Cannot cancel order in current status'}

        try:
            with transaction.atomic():
                # Restore stock for each item
                for item in self.items.all():
                    item.product.update_stock(
                        quantity_change=item.quantity,
                        transaction_type='cancellation',
                        reference_id=self.id,
                        notes=f"Order {self.order_number} cancelled"
                    )

                self.status = 'cancelled'
                self.save()

                return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @classmethod
    def get_orders_by_customer(cls, customer_id):
        """Get all orders for a customer."""
        return cls.objects.filter(customer_id=customer_id).order_by('-created_at')

    @classmethod
    def get_recent_orders(cls, limit=10):
        """Get most recent orders."""
        return cls.objects.select_related('customer').order_by('-created_at')[:limit]

    @classmethod
    def get_order_stats(cls):
        """Get order statistics for reports."""
        from django.db.models import Sum, Count, Avg

        all_orders = cls.objects.all()

        # Total revenue (exclude cancelled)
        total_revenue = cls.objects.exclude(status='cancelled').aggregate(
            total=Sum('total')
        )['total'] or 0

        # Total orders (exclude delivered, cancelled, refunded for "active" count)
        total_orders = cls.objects.exclude(
            status__in=['delivered', 'cancelled', 'refunded']
        ).count()

        # Average order value
        avg_order = cls.objects.exclude(status='cancelled').aggregate(
            avg=Avg('total')
        )['avg'] or 0

        # Orders by status
        by_status = {}
        for status, _ in cls.STATUS_CHOICES:
            count = cls.objects.filter(status=status).count()
            if count > 0:
                revenue = cls.objects.filter(status=status).aggregate(
                    total=Sum('total')
                )['total'] or 0
                by_status[status] = {'count': count, 'revenue': revenue}

        return {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'average_order_value': avg_order,
            'by_status': by_status,
        }


class OrderItem(models.Model):
    """
    Order item model for ShopPy e-commerce system.
    Mirrors the Perl order_items table structure.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True
    )
    product_name = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class InventoryTransaction(models.Model):
    """
    Inventory transaction model for tracking stock changes.
    Mirrors the Perl inventory_transactions table structure.
    """

    TRANSACTION_TYPES = [
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
        ('restock', 'Restock'),
        ('cancellation', 'Cancellation'),
    ]

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='inventory_transactions'
    )
    quantity_change = models.IntegerField()
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    reference_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'inventory_transactions'
        verbose_name = 'Inventory Transaction'
        verbose_name_plural = 'Inventory Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type}: {self.product.name} ({self.quantity_change:+d})"
