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
from functools import wraps

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
    categories = PRODUCT_CATEGORIES
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
    categories = PRODUCT_CATEGORIES

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

    # Get order stats
    stats = Order.get_order_stats()

    # Get top customers
    top_customers = Customer.objects.annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total')
    ).filter(order_count__gt=0).order_by('-total_spent')[:10]

    # Add email to customer data
    top_customers_data = []
    for cust in top_customers:
        top_customers_data.append({
            'first_name': cust.first_name,
            'last_name': cust.last_name,
            'email': cust.user.email if cust.user else '',
            'order_count': cust.order_count,
            'total_spent': cust.total_spent or 0,
        })

    return render(request, 'admin/reports.html', {
        'stats': stats,
        'top_customers': top_customers_data,
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

    # Orders - Admin
    path('orders/<int:order_id>/update-status/', order_update_status, name='admin_order_update_status'),
    path('orders/<int:order_id>/update-status/', order_update_status, name='order_update_status'),
    path('orders/<int:order_id>/delete/', order_delete, name='admin_order_delete'),
    path('orders/<int:order_id>/delete/', order_delete, name='order_delete'),

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
