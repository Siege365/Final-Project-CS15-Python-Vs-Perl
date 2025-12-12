"""
ShopPy - Customer Routes
Routes for customer users only.
Equivalent to Perl routes/customer_routes.pl
"""

from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from functools import wraps

from lib.ECommerce.Auth import Auth
from lib.ECommerce.Models.Product import Product
from lib.ECommerce.Models.Order import Order
from lib.ECommerce.Models.Customer import Customer
from lib.ECommerce.Config import APP_CONFIG


def customer_required(view_func):
    """Decorator to require customer role."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'customer':
            messages.error(request, 'This page is for customers only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# =============================================================================
# CART
# =============================================================================

@login_required
def cart(request):
    """View shopping cart."""
    cart_items = request.session.get('cart', [])

    # Ensure each cart item has an image_url
    for item in cart_items:
        if not item.get('image_url'):
            try:
                product = Product.objects.get(id=item['product_id'])
                item['image_url'] = product.image_url
            except Product.DoesNotExist:
                item['image_url'] = ''

    # Get customer's address
    customer_address = ''
    customer_id = Auth.get_customer_id(request)
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            customer_address = customer.address
        except Customer.DoesNotExist:
            pass

    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    tax_rate = APP_CONFIG.get('tax_rate', 0.08)
    shipping_rate = APP_CONFIG.get('shipping_rate', 5.00)
    free_shipping_threshold = APP_CONFIG.get('free_shipping_threshold', 100.00)

    tax = subtotal * tax_rate
    shipping = 0 if subtotal >= free_shipping_threshold else shipping_rate
    total = subtotal + tax + shipping

    return render(request, 'customer/cart.html', {
        'cart': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'tax_rate': tax_rate * 100,
        'shipping': shipping,
        'total': total,
        'customer_address': customer_address,
        'free_shipping_threshold': free_shipping_threshold,
        'role': request.user.role,
    })


@login_required
@require_POST
def cart_add(request):
    """Add item to cart."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Product not found'})
        messages.error(request, 'Product not found')
        return redirect('products')

    cart = request.session.get('cart', [])

    # Check if product already in cart
    found = False
    for item in cart:
        if str(item['product_id']) == str(product_id):
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart.append({
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image_url': product.image_url,
        })

    request.session['cart'] = cart

    # Calculate cart count (distinct products)
    cart_count = len(cart)

    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'product_name': product.name,
            'cart_count': cart_count
        })

    messages.success(request, 'Product added to cart!')
    return redirect('products')


@login_required
@require_POST
def cart_remove(request):
    """Remove item from cart."""
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', [])

    # Filter out the product to remove
    cart = [item for item in cart if str(item['product_id']) != str(product_id)]
    request.session['cart'] = cart

    messages.success(request, 'Product removed from cart')
    return redirect('cart')


@login_required
@require_POST
def api_cart_add(request):
    """API endpoint for adding to cart via JSON."""
    import json
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    
    # Check stock
    if product.stock_quantity < quantity:
        return JsonResponse({'success': False, 'message': 'Not enough stock available'})
    
    cart = request.session.get('cart', [])
    
    # Check if product already in cart
    found = False
    for item in cart:
        if str(item['product_id']) == str(product_id):
            item['quantity'] += quantity
            found = True
            break
    
    if not found:
        cart.append({
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image_url': product.image_url or '',
        })
    
    request.session['cart'] = cart
    request.session.modified = True
    
    # Calculate cart count
    cart_count = sum(item['quantity'] for item in cart)
    
    return JsonResponse({
        'success': True,
        'product_name': product.name,
        'cart_count': cart_count
    })


# =============================================================================
# CHECKOUT
# =============================================================================

@login_required
@require_POST
def checkout(request):
    """Process checkout."""
    cart = request.session.get('cart', [])

    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    # Get or create customer record
    customer_id = Auth.get_customer_id(request)

    if not customer_id:
        # Try to get customer by user_id
        customer = Customer.get_customer_by_user_id(request.user.id)

        if customer:
            customer_id = customer.id
            request.session['customer_id'] = customer_id
        else:
            # Create customer profile
            customer = Customer.objects.create(
                user=request.user,
                first_name=request.user.username,
                last_name='',
                phone='',
                address=''
            )
            customer_id = customer.id
            request.session['customer_id'] = customer_id

    # Get checkout form data
    payment_method = request.POST.get('payment_method', '')
    shipping_address = request.POST.get('shipping_address', '')

    # Create order
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found')
        return redirect('cart')

    result = Order.create_from_cart(
        customer=customer,
        cart_items=cart,
        payment_method=payment_method,
        shipping_address=shipping_address
    )

    if result['success']:
        # Clear cart
        request.session['cart'] = []
        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', order_id=result['order_id'])
    else:
        messages.error(request, result['message'])
        return redirect('cart')


# =============================================================================
# ORDER CANCELLATION
# =============================================================================

@customer_required
@require_POST
def order_cancel(request, order_id):
    """Cancel an order."""
    order = get_object_or_404(Order, id=order_id)

    # Verify order belongs to customer
    customer_id = Auth.get_customer_id(request)
    if order.customer_id != customer_id:
        messages.error(request, 'Access denied')
        return redirect('orders')

    if order.status != 'pending':
        messages.error(request, 'Only pending orders can be cancelled')
        return redirect('order_detail', order_id=order_id)

    result = order.cancel_order()

    if result['success']:
        messages.success(request, 'Order cancelled successfully')
    else:
        messages.error(request, result.get('message', 'Failed to cancel order'))

    return redirect('order_detail', order_id=order_id)


# =============================================================================
# ACCOUNT
# =============================================================================

@customer_required
def account(request):
    """View account details."""
    customer_id = Auth.get_customer_id(request)

    if customer_id:
        try:
            customer = Customer.objects.select_related('user').get(id=customer_id)
        except Customer.DoesNotExist:
            customer = None
    else:
        customer = None

    return render(request, 'customer/account.html', {
        'customer': customer,
        'role': request.user.role,
    })


@customer_required
@require_POST
def account_update(request):
    """Update account details."""
    customer_id = Auth.get_customer_id(request)

    if not customer_id:
        messages.error(request, 'Customer profile not found')
        return redirect('account')

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found')
        return redirect('account')

    # Update customer details
    customer.first_name = request.POST.get('first_name', customer.first_name)
    customer.last_name = request.POST.get('last_name', customer.last_name)
    customer.phone = request.POST.get('phone', customer.phone)
    customer.address = request.POST.get('address', customer.address)
    customer.city = request.POST.get('city', customer.city)
    customer.state = request.POST.get('state', customer.state)
    customer.zip_code = request.POST.get('zip_code', customer.zip_code)

    try:
        customer.save()
        messages.success(request, 'Account updated successfully!')
    except Exception as e:
        messages.error(request, f'Failed to update account: {str(e)}')

    return redirect('account')


@customer_required
@require_POST
def account_delete(request):
    """Delete account."""
    customer_id = Auth.get_customer_id(request)

    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            user = customer.user
            customer.delete()
            if user:
                user.delete()
        except Customer.DoesNotExist:
            pass

    # Logout user
    Auth.logout_user(request)
    messages.success(request, 'Account deleted successfully')
    return redirect('home')


# =============================================================================
# URL PATTERNS
# =============================================================================

urlpatterns = [
    # Cart
    path('cart/', cart, name='cart'),
    path('cart/', cart, name='customer_cart'),
    path('cart/add/', cart_add, name='cart_add'),
    path('cart/add/', cart_add, name='customer_cart_add'),
    path('cart/remove/', cart_remove, name='cart_remove'),
    path('cart/remove/', cart_remove, name='customer_cart_remove'),
    
    # Cart API (for AJAX)
    path('api/cart/add/', api_cart_add, name='api_cart_add'),

    # Checkout
    path('checkout/', checkout, name='checkout'),
    path('checkout/', checkout, name='customer_checkout'),

    # Order cancellation
    path('orders/<int:order_id>/cancel/', order_cancel, name='order_cancel'),
    path('orders/<int:order_id>/cancel/', order_cancel, name='customer_order_cancel'),

    # Account
    path('account/', account, name='account'),
    path('account/', account, name='customer_account'),
    path('account/update/', account_update, name='account_update'),
    path('account/update/', account_update, name='customer_account_update'),
    path('account/delete/', account_delete, name='account_delete'),
    path('account/delete/', account_delete, name='customer_account_delete'),
]
