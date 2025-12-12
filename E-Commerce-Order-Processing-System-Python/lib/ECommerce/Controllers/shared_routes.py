"""
ShopPy - Shared Routes
Routes accessible by both admin and customer users.
Equivalent to Perl routes/shared_routes.pl
"""

from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from lib.ECommerce.Auth import Auth
from lib.ECommerce.Models.User import User
from lib.ECommerce.Models.Customer import Customer
from lib.ECommerce.Models.Product import Product
from lib.ECommerce.Models.Order import Order
from lib.ECommerce.Config import APP_CONFIG


# =============================================================================
# HOME / LOGIN
# =============================================================================

def home(request):
    """Home page - login form or redirect to dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')


@require_POST
def login_view(request):
    """Handle login POST request."""
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = Auth.login_user(request, username, password)

    if user:
        messages.success(request, 'Login successful!')
        return redirect('dashboard')
    else:
        messages.error(request, 'Invalid username or password')
        return redirect('home')


def logout_view(request):
    """Handle logout."""
    Auth.logout_user(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


# =============================================================================
# REGISTRATION
# =============================================================================

def register(request):
    """Show registration form."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'customer/register.html')


@require_POST
def register_submit(request):
    """Handle registration form submission."""
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    phone = request.POST.get('phone', '')
    address = request.POST.get('address', '')
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')

    if password != confirm_password:
        messages.error(request, 'Passwords do not match')
        return redirect('register')

    result = Auth.register_user(
        username=username,
        email=email,
        password=password,
        role='customer',
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        address=address
    )

    if result['success']:
        messages.success(request, 'Registration successful! Please login.')
        return redirect('home')
    else:
        messages.error(request, result['message'])
        return redirect('register')


# =============================================================================
# DASHBOARD (Role-based)
# =============================================================================

@login_required
def dashboard(request):
    """Dashboard view - role-based."""
    from django.db.models import Sum
    
    user = request.user
    role = user.role

    if role in ['admin', 'staff']:
        # Admin/Staff Dashboard
        import django.db.models as models
        
        page = int(request.GET.get('page', 1))
        per_page = 10

        total_products = Product.objects.filter(is_active=True).count()
        low_stock = Product.objects.filter(
            is_active=True,
            stock_quantity__lte=models.F('reorder_level')
        ).count() if hasattr(Product, 'objects') else Product.get_low_stock_products().count()

        # Get recent orders with pagination
        all_orders = Order.objects.select_related('customer').order_by('-created_at')
        total_orders = all_orders.exclude(status__in=['delivered', 'cancelled', 'refunded']).count()
        total_customers = Customer.objects.count()

        # Paginate recent orders
        start = (page - 1) * per_page
        end = start + per_page
        recent_orders = all_orders[start:end]
        total_pages = (all_orders.count() + per_page - 1) // per_page

        stats = {
            'total_products': total_products,
            'low_stock': low_stock,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'recent_orders': recent_orders,
            'page': page,
            'total_pages': total_pages,
        }

        return render(request, 'admin/dashboard_admin.html', {
            'stats': stats,
            'role': role,
        })
    else:
        # Customer Dashboard
        customer_id = Auth.get_customer_id(request)

        if customer_id:
            page = int(request.GET.get('page', 1))
            per_page = 10

            orders = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
            total_orders = orders.count()
            pending_orders = orders.filter(status='pending').count()
            delivered_orders = orders.filter(status='delivered').count()

            total_spent = orders.exclude(status='cancelled').aggregate(
                total=Sum('total')
            )['total'] or 0

            # Paginate orders
            start = (page - 1) * per_page
            end = start + per_page
            recent_orders = orders[start:end]
            total_pages = (total_orders + per_page - 1) // per_page

            stats = {
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'delivered_orders': delivered_orders,
                'total_spent': total_spent,
                'recent_orders': recent_orders,
                'page': page,
                'total_pages': total_pages,
            }
        else:
            stats = {
                'total_orders': 0,
                'pending_orders': 0,
                'delivered_orders': 0,
                'total_spent': 0,
                'recent_orders': [],
                'page': 1,
                'total_pages': 1,
            }

        return render(request, 'customer/dashboard_customer.html', {
            'stats': stats,
            'role': role,
        })


# =============================================================================
# PRODUCTS (Role-based)
# =============================================================================

@login_required
def products(request):
    """Products list view - role-based."""
    user = request.user
    role = user.role

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', '')
    page = int(request.GET.get('page', 1))
    per_page = 10

    # Get categories
    categories = Product.get_categories()

    # Get products
    if search:
        products_list = Product.search_products(search, active_only=(role == 'customer'))
    elif category:
        products_list = Product.get_products_by_category(category, active_only=(role == 'customer'))
    else:
        if role == 'customer':
            products_list = Product.get_active_products()
        else:
            products_list = Product.objects.all().order_by('id')

    # Sort products (admin/staff only)
    if sort and role in ['admin', 'staff']:
        if sort == 'in_stock':
            products_list = products_list.filter(stock_quantity__gt=15).order_by('-stock_quantity')
        elif sort == 'low_stock':
            products_list = products_list.filter(
                stock_quantity__gt=0,
                stock_quantity__lte=15
            ).order_by('stock_quantity')
        elif sort == 'out_of_stock':
            products_list = products_list.filter(stock_quantity=0)
        else:
            products_list = products_list.order_by('id')

    # Pagination
    total = products_list.count()
    start = (page - 1) * per_page
    end = start + per_page
    products_page = products_list[start:end]
    total_pages = (total + per_page - 1) // per_page
    has_more = end < total
    next_page = page + 1 if has_more else None

    # Handle AJAX request for infinite scroll
    if request.GET.get('ajax') == '1' and role == 'customer':
        products_data = []
        for p in products_page:
            products_data.append({
                'id': p.id,
                'name': p.name,
                'description': p.description[:100] + '...' if len(p.description) > 100 else p.description,
                'category': p.category,
                'price': float(p.price),
                'stock': p.stock_quantity,
                'image_url': p.image_url or '',
            })
        return JsonResponse({
            'products': products_data,
            'has_more': has_more,
            'next_page': next_page,
        })

    # Generate page range for pagination (admin only)
    page_range = range(1, total_pages + 1)

    context = {
        'products': products_page,
        'categories': categories,
        'sort': sort,
        'page': page,
        'total_pages': total_pages,
        'total_products': total,
        'page_range': page_range,
        'has_more': has_more,
        'next_page': next_page,
        'role': role,
    }

    if role in ['admin', 'staff']:
        return render(request, 'admin/products_admin.html', context)
    else:
        return render(request, 'customer/products_customer.html', context)


# =============================================================================
# ORDERS (Role-based)
# =============================================================================

@login_required
def orders(request):
    """Orders list view - role-based."""
    user = request.user
    role = user.role

    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    page = int(request.GET.get('page', 1))
    per_page = 10

    if role in ['admin', 'staff']:
        orders_list = Order.objects.select_related('customer').order_by('-created_at')
    else:
        customer_id = Auth.get_customer_id(request)
        if customer_id:
            orders_list = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
        else:
            orders_list = Order.objects.none()

    # Search filter
    if search:
        from django.db.models import Q
        orders_list = orders_list.filter(
            Q(order_number__icontains=search) |
            Q(status__icontains=search) |
            Q(payment_method__icontains=search)
        )

    # Sort
    if sort:
        if sort == 'recent':
            orders_list = orders_list.order_by('-id')
        elif sort == 'earliest':
            orders_list = orders_list.order_by('id')
        elif sort in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
            orders_list = orders_list.filter(status=sort)

    # Pagination
    total = orders_list.count()
    start = (page - 1) * per_page
    end = start + per_page
    orders_page = orders_list[start:end]
    total_pages = (total + per_page - 1) // per_page

    context = {
        'orders': orders_page,
        'sort': sort,
        'page': page,
        'total_pages': total_pages,
        'role': role,
    }

    if role in ['admin', 'staff']:
        return render(request, 'admin/orders_admin.html', context)
    else:
        return render(request, 'customer/orders_customer.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail view - role-based."""
    user = request.user
    role = user.role

    try:
        order = Order.objects.select_related('customer').prefetch_related('items').get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('orders')

    # Customers can only view their own orders
    if role == 'customer':
        customer_id = Auth.get_customer_id(request)
        if order.customer_id != customer_id:
            messages.error(request, 'Access denied')
            return redirect('orders')

    context = {
        'order': order,
        'items': order.items.all(),
        'role': role,
    }

    if role in ['admin', 'staff']:
        return render(request, 'admin/order_detail_admin.html', context)
    else:
        return render(request, 'customer/order_detail_customer.html', context)


# =============================================================================
# API ENDPOINTS
# =============================================================================

@login_required
@require_GET
def api_products(request):
    """API endpoint for infinite scroll products."""
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    page = int(request.GET.get('page', 1))
    per_page = 10

    if search:
        products = Product.search_products(search)
    elif category:
        products = Product.get_products_by_category(category)
    else:
        products = Product.get_active_products()

    # Pagination
    total = products.count()
    start = (page - 1) * per_page
    end = start + per_page
    products_page = products[start:end]
    has_more = end < total

    # Serialize products
    products_data = []
    for p in products_page:
        products_data.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'sku': p.sku,
            'category': p.category,
            'price': float(p.price),
            'stock_quantity': p.stock_quantity,
            'reorder_level': p.reorder_level,
            'image_url': p.image_url,
        })

    return JsonResponse({
        'products': products_data,
        'has_more': has_more
    })


# =============================================================================
# URL PATTERNS
# =============================================================================

# Import models for dashboard queries
from django.db import models

urlpatterns = [
    # Home / Auth
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('register/submit/', register_submit, name='register_submit'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='admin_dashboard'),
    path('dashboard/', dashboard, name='customer_dashboard'),

    # Products (shared view - role-based templates)
    path('products/', products, name='products'),
    path('products/', products, name='admin_products'),
    path('products/', products, name='customer_products'),

    # Orders (shared view - role-based templates)
    path('orders/', orders, name='orders'),
    path('orders/', orders, name='admin_orders'),
    path('orders/', orders, name='customer_orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/<int:order_id>/', order_detail, name='admin_order_detail'),
    path('orders/<int:order_id>/', order_detail, name='customer_order_detail'),

    # API
    path('api/products/', api_products, name='api_products'),
]
