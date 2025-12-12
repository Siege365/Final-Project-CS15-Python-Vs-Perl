"""
ShopPy - Admin Routes
Routes for admin and staff users only.
Equivalent to Perl routes/admin_routes.pl
"""

from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import models
from functools import wraps
import json

from lib.ECommerce.Models.Product import Product
from lib.ECommerce.Models.Order import Order
from lib.ECommerce.Models.Customer import Customer
from lib.ECommerce.Config import PRODUCT_CATEGORIES, ORDER_STATUS


def admin_required(view_func):
    """Decorator to require admin or staff role."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['admin', 'staff']:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# =============================================================================
# PRODUCT MANAGEMENT
# =============================================================================

@admin_required
def product_add(request):
    """Show add product form."""
    # Extract category values from tuples
    categories = [cat[0] for cat in PRODUCT_CATEGORIES]
    return render(request, 'admin/product_add.html', {
        'categories': categories,
        'role': request.user.role,
    })


@admin_required
@require_POST
def product_add_submit(request):
    """Handle add product form submission."""
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    sku = request.POST.get('sku', '')
    category = request.POST.get('category', '')
    price = request.POST.get('price', 0)
    cost = request.POST.get('cost', 0)
    stock_quantity = request.POST.get('stock_quantity', 0)
    reorder_level = request.POST.get('reorder_level', 10)
    image_url = request.POST.get('image_url', '')

    # Check for duplicate SKU
    if Product.objects.filter(sku=sku).exists():
        messages.error(request, f"Product with SKU '{sku}' already exists")
        return redirect('product_add')

    try:
        Product.objects.create(
            name=name,
            description=description,
            sku=sku,
            category=category,
            price=price,
            cost=cost or 0,
            stock_quantity=stock_quantity or 0,
            reorder_level=reorder_level or 10,
            image_url=image_url
        )
        messages.success(request, 'Product created successfully!')
        return redirect('products')
    except Exception as e:
        messages.error(request, f'Failed to create product: {str(e)}')
        return redirect('product_add')


@admin_required
def product_edit(request, product_id):
    """Show edit product form."""
    product = get_object_or_404(Product, id=product_id)
    # Extract category values from tuples
    categories = [cat[0] for cat in PRODUCT_CATEGORIES]

    return render(request, 'admin/product_edit.html', {
        'product': product,
        'categories': categories,
        'role': request.user.role,
    })


@admin_required
@require_POST
def product_edit_submit(request, product_id):
    """Handle edit product form submission."""
    product = get_object_or_404(Product, id=product_id)

    product.name = request.POST.get('name', product.name)
    product.description = request.POST.get('description', product.description)
    new_sku = request.POST.get('sku', product.sku)

    # Check for duplicate SKU if changed
    if new_sku != product.sku and Product.objects.filter(sku=new_sku).exists():
        messages.error(request, f"Product with SKU '{new_sku}' already exists")
        return redirect('product_edit', product_id=product_id)

    product.sku = new_sku
    product.category = request.POST.get('category', product.category)
    product.price = request.POST.get('price', product.price)
    product.cost = request.POST.get('cost', product.cost) or 0
    product.stock_quantity = request.POST.get('stock_quantity', product.stock_quantity) or 0
    product.reorder_level = request.POST.get('reorder_level', product.reorder_level) or 10
    product.image_url = request.POST.get('image_url', product.image_url)

    try:
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('products')
    except Exception as e:
        messages.error(request, f'Failed to update product: {str(e)}')
        return redirect('product_edit', product_id=product_id)


@admin_required
@require_POST
def product_delete(request, product_id):
    """Handle product deletion (soft delete)."""
    product = get_object_or_404(Product, id=product_id)
    product.is_active = False
    product.save()
    messages.success(request, 'Product deleted successfully!')
    return redirect('products')


@admin_required
@require_POST
def product_adjust_stock(request, product_id):
    """Handle quick stock adjustment."""
    product = get_object_or_404(Product, id=product_id)
    
    adjustment_type = request.POST.get('adjustment_type', 'set')
    quantity = request.POST.get('quantity', 0)
    
    try:
        quantity = int(quantity)
        if quantity < 0:
            messages.error(request, 'Quantity cannot be negative')
            return redirect('products')
        
        old_stock = product.stock_quantity
        
        if adjustment_type == 'add':
            product.stock_quantity += quantity
        elif adjustment_type == 'remove':
            product.stock_quantity = max(0, product.stock_quantity - quantity)
        elif adjustment_type == 'set':
            product.stock_quantity = quantity
        else:
            messages.error(request, 'Invalid adjustment type')
            return redirect('products')
        
        product.save()
        
        # Create a meaningful success message
        if adjustment_type == 'add':
            messages.success(request, f'Added {quantity} units to {product.name}. Stock: {old_stock} → {product.stock_quantity}')
        elif adjustment_type == 'remove':
            messages.success(request, f'Removed {quantity} units from {product.name}. Stock: {old_stock} → {product.stock_quantity}')
        else:
            messages.success(request, f'Set stock for {product.name} to {product.stock_quantity}')
        
        return redirect('products')
        
    except ValueError:
        messages.error(request, 'Invalid quantity value')
        return redirect('products')
    except Exception as e:
        messages.error(request, f'Failed to adjust stock: {str(e)}')
        return redirect('products')


# =============================================================================
# ORDER MANAGEMENT
# =============================================================================

@admin_required
@require_POST
def order_update_status(request, order_id):
    """Update order status."""
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status', '')

    if new_status:
        order.status = new_status
        order.save()
        messages.success(request, f'Order status updated to {new_status}')

    return redirect('order_detail', order_id=order_id)


@admin_required
@require_POST
def api_order_update_status(request):
    """API endpoint to update order status (returns JSON)."""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        if not order_id or not new_status:
            return JsonResponse({
                'success': False,
                'message': 'Order ID and status are required'
            }, status=400)
        
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Order status updated to {new_status}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@admin_required
@require_POST
def api_order_bulk_update(request):
    """API endpoint to bulk update order statuses (returns JSON)."""
    try:
        data = json.loads(request.body)
        order_ids = data.get('order_ids', [])
        new_status = data.get('status')
        
        if not order_ids or not new_status:
            return JsonResponse({
                'success': False,
                'message': 'Order IDs and status are required'
            }, status=400)
        
        updated_count = Order.objects.filter(id__in=order_ids).update(status=new_status)
        
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} order(s) updated to {new_status}',
            'count': updated_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@admin_required
@require_POST
def order_delete(request, order_id):
    """Delete an order."""
    order = get_object_or_404(Order, id=order_id)

    # Delete order items first
    order.items.all().delete()
    order.delete()

    messages.success(request, 'Order deleted successfully!')
    return redirect('orders')


# =============================================================================
# CUSTOMER MANAGEMENT
# =============================================================================

@admin_required
def customers(request):
    """List all customers."""
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    per_page = 20

    if search:
        customers_list = Customer.search_customers(search)
    else:
        customers_list = Customer.objects.select_related('user').order_by('-created_at')

    # Pagination
    total = customers_list.count()
    start = (page - 1) * per_page
    end = start + per_page
    customers_page = customers_list[start:end]
    total_pages = (total + per_page - 1) // per_page

    return render(request, 'admin/customers.html', {
        'customers': customers_page,
        'page': page,
        'total_pages': total_pages,
        'role': request.user.role,
    })


@admin_required
@require_POST
def customer_delete(request, customer_id):
    """Delete a customer."""
    customer = get_object_or_404(Customer, id=customer_id)

    # Also delete associated user if exists
    if customer.user:
        customer.user.delete()

    customer.delete()
    messages.success(request, 'Customer deleted successfully!')
    return redirect('customers')


@admin_required
def customer_detail(request, customer_id):
    """View customer details."""
    customer = get_object_or_404(Customer.objects.select_related('user'), id=customer_id)
    
    # Get customer's orders
    orders = Order.objects.filter(customer=customer).order_by('-created_at')[:10]
    
    # Calculate stats
    from django.db.models import Sum, Count
    stats = Order.objects.filter(customer=customer).aggregate(
        total_orders=Count('id'),
        total_spent=Sum('total')
    )
    
    return render(request, 'admin/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'stats': stats,
        'role': request.user.role,
    })


# =============================================================================
# REPORTS
# =============================================================================

@admin_required
def reports(request):
    """Show reports and analytics."""
    from django.db.models import Sum, Count, F
    from django.utils import timezone
    from datetime import timedelta
    import json

    # Get date range parameters
    period = request.GET.get('period', 'month')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Calculate date range
    today = timezone.now().date()
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
        end_date = today
    elif period == 'month':
        start_date = today - timedelta(days=30)
        end_date = today
    elif period == 'quarter':
        start_date = today - timedelta(days=90)
        end_date = today
    elif period == 'year':
        start_date = today - timedelta(days=365)
        end_date = today
    elif period == 'custom' and date_from and date_to:
        from datetime import datetime
        start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
    else:
        start_date = today - timedelta(days=30)
        end_date = today

    # Filter orders by date range
    orders_in_range = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )

    # Total revenue (exclude cancelled)
    total_revenue = orders_in_range.exclude(status='cancelled').aggregate(
        total=Sum('total')
    )['total'] or 0

    # Total orders
    total_orders = orders_in_range.count()

    # Average order value
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Products sold
    from lib.ECommerce.Models.Order import OrderItem
    products_sold = OrderItem.objects.filter(
        order__in=orders_in_range
    ).aggregate(total=Sum('quantity'))['total'] or 0
    
    unique_products = OrderItem.objects.filter(
        order__in=orders_in_range
    ).values('product').distinct().count()

    # New customers in period
    new_customers = Customer.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).count()
    
    # Returning customers (customers with orders before and during period)
    returning_customers = 0  # Simplified for now

    # Top products
    top_products_data = OrderItem.objects.filter(
        order__in=orders_in_range.exclude(status='cancelled')
    ).values('product_name').annotate(
        quantity_sold=Sum('quantity'),
        revenue=Sum('subtotal')
    ).order_by('-revenue')[:10]
    
    top_products = [
        {
            'name': p['product_name'],
            'quantity_sold': p['quantity_sold'],
            'revenue': float(p['revenue'] or 0)
        }
        for p in top_products_data
    ]

    # Top customers
    top_customers = Customer.objects.annotate(
        order_count=Count('orders', filter=models.Q(
            orders__created_at__date__gte=start_date,
            orders__created_at__date__lte=end_date
        )),
        total_spent=Sum('orders__total', filter=models.Q(
            orders__created_at__date__gte=start_date,
            orders__created_at__date__lte=end_date,
        ) & ~models.Q(orders__status='cancelled'))
    ).filter(order_count__gt=0).order_by('-total_spent')[:10]

    top_customers_list = [
        {
            'first_name': c.first_name,
            'last_name': c.last_name,
            'order_count': c.order_count,
            'total_spent': float(c.total_spent or 0)
        }
        for c in top_customers
    ]

    # Chart data - Revenue over time
    revenue_by_day = orders_in_range.exclude(status='cancelled').extra(
        select={'day': 'DATE(created_at)'}
    ).values('day').annotate(
        daily_revenue=Sum('total')
    ).order_by('day')
    
    revenue_labels = [str(r['day']) for r in revenue_by_day]
    revenue_data = [float(r['daily_revenue'] or 0) for r in revenue_by_day]
    
    # If no data, provide empty arrays
    if not revenue_labels:
        revenue_labels = [str(start_date)]
        revenue_data = [0]

    # Category sales data
    category_sales = OrderItem.objects.filter(
        order__in=orders_in_range.exclude(status='cancelled')
    ).values('product__category').annotate(
        total=Sum('subtotal')
    ).order_by('-total')[:6]
    
    category_labels = [c['product__category'] or 'Uncategorized' for c in category_sales]
    category_data = [float(c['total'] or 0) for c in category_sales]
    
    if not category_labels:
        category_labels = ['No Data']
        category_data = [0]

    # Status distribution
    status_counts = orders_in_range.values('status').annotate(count=Count('id'))
    status_map = {'pending': 0, 'processing': 0, 'shipped': 0, 'delivered': 0, 'cancelled': 0}
    for s in status_counts:
        if s['status'] in status_map:
            status_map[s['status']] = s['count']
    status_data = [status_map['pending'], status_map['processing'], status_map['shipped'], status_map['delivered'], status_map['cancelled']]

    # Build report data
    report = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'average_order_value': avg_order_value,
        'products_sold': products_sold,
        'unique_products': unique_products,
        'new_customers': new_customers,
        'returning_customers': returning_customers,
        'top_products': top_products,
        'top_customers': top_customers_list,
    }

    # Chart data for JavaScript
    chart_data = {
        'revenue_labels': json.dumps(revenue_labels),
        'revenue_data': json.dumps(revenue_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'status_data': json.dumps(status_data),
    }

    return render(request, 'admin/reports.html', {
        'report': report,
        'chart_data': chart_data,
        'period': period,
        'date_from': date_from,
        'date_to': date_to,
        'role': request.user.role,
    })


# =============================================================================
# URL PATTERNS
# =============================================================================

urlpatterns = [
    # Products - Admin
    path('products/add/', product_add, name='admin_product_add'),
    path('products/add/', product_add, name='product_add'),
    path('products/add/submit/', product_add_submit, name='admin_product_add_submit'),
    path('products/<int:product_id>/edit/', product_edit, name='admin_product_edit'),
    path('products/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('products/<int:product_id>/edit/submit/', product_edit_submit, name='admin_product_edit_submit'),
    path('products/<int:product_id>/edit/submit/', product_edit_submit, name='product_edit_submit'),
    path('products/<int:product_id>/delete/', product_delete, name='admin_product_delete'),
    path('products/<int:product_id>/delete/', product_delete, name='product_delete'),
    path('products/<int:product_id>/adjust-stock/', product_adjust_stock, name='admin_product_adjust_stock'),
    path('products/<int:product_id>/adjust-stock/', product_adjust_stock, name='product_adjust_stock'),

    # Orders - Admin
    path('orders/<int:order_id>/update-status/', order_update_status, name='admin_order_update_status'),
    path('orders/<int:order_id>/update-status/', order_update_status, name='order_update_status'),
    path('orders/<int:order_id>/delete/', order_delete, name='admin_order_delete'),
    path('orders/<int:order_id>/delete/', order_delete, name='order_delete'),
    
    # Order API endpoints
    path('api/orders/update-status/', api_order_update_status, name='api_order_update_status'),
    path('api/orders/bulk-update/', api_order_bulk_update, name='api_order_bulk_update'),

    # Customers - Admin
    path('customers/', customers, name='admin_customers'),
    path('customers/', customers, name='customers'),
    path('customers/<int:customer_id>/', customer_detail, name='admin_customer_detail'),
    path('customers/<int:customer_id>/', customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/delete/', customer_delete, name='admin_customer_delete'),
    path('customers/<int:customer_id>/delete/', customer_delete, name='customer_delete'),

    # Reports - Admin
    path('reports/', reports, name='admin_reports'),
    path('reports/', reports, name='reports'),
]
