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

    # Ensure each cart item has an image_url and calculate subtotal
    for item in cart_items:
        if not item.get('image_url'):
            try:
                product = Product.objects.get(id=item['product_id'])
                item['image_url'] = product.image_url
            except Product.DoesNotExist:
                item['image_url'] = ''
        # Calculate item subtotal
        item['subtotal'] = float(item['price']) * int(item['quantity'])

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
        'cart_items': cart_items,
        'cart_count': len(cart_items),
        'cart_subtotal': subtotal,
        'cart_tax': tax,
        'tax_rate': tax_rate * 100,
        'cart_shipping': shipping,
        'cart_total': total,
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
    
    # Calculate cart count (distinct products)
    cart_count = len(cart)
    
    return JsonResponse({
        'success': True,
        'product_name': product.name,
        'cart_count': cart_count
    })


@login_required
@require_POST
def api_cart_update(request):
    """API endpoint for updating cart item quantity."""
    import json
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    
    if quantity < 1:
        return JsonResponse({'success': False, 'message': 'Invalid quantity'})
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    
    # Check stock
    if product.stock_quantity < quantity:
        return JsonResponse({'success': False, 'message': 'Not enough stock available'})
    
    cart = request.session.get('cart', [])
    
    # Update quantity for the product
    found = False
    for item in cart:
        if str(item['product_id']) == str(product_id):
            item['quantity'] = quantity
            item['subtotal'] = float(item['price']) * quantity
            found = True
            break
    
    if not found:
        return JsonResponse({'success': False, 'message': 'Product not in cart'})
    
    request.session['cart'] = cart
    request.session.modified = True
    
    # Calculate totals
    subtotal = sum(float(item['price']) * int(item['quantity']) for item in cart)
    tax_rate = APP_CONFIG.get('tax_rate', 0.08)
    shipping_rate = APP_CONFIG.get('shipping_rate', 5.00)
    free_shipping_threshold = APP_CONFIG.get('free_shipping_threshold', 100.00)
    
    tax = subtotal * tax_rate
    shipping = 0 if subtotal >= free_shipping_threshold else shipping_rate
    total = subtotal + tax + shipping
    
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'items': cart,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'free_shipping': subtotal >= free_shipping_threshold,
        'total': total
    })


@login_required
@require_POST
def api_cart_remove(request):
    """API endpoint for removing item from cart."""
    import json
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    
    cart = request.session.get('cart', [])
    
    # Filter out the product to remove
    cart = [item for item in cart if str(item['product_id']) != str(product_id)]
    request.session['cart'] = cart
    request.session.modified = True
    
    # Calculate totals
    subtotal = sum(float(item['price']) * int(item['quantity']) for item in cart)
    tax_rate = APP_CONFIG.get('tax_rate', 0.08)
    shipping_rate = APP_CONFIG.get('shipping_rate', 5.00)
    free_shipping_threshold = APP_CONFIG.get('free_shipping_threshold', 100.00)
    
    tax = subtotal * tax_rate
    shipping = 0 if subtotal >= free_shipping_threshold else shipping_rate
    total = subtotal + tax + shipping
    
    return JsonResponse({
        'success': True,
        'cart_count': len(cart),
        'items': cart,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'free_shipping': subtotal >= free_shipping_threshold,
        'total': total
    })


@login_required
@require_POST
def api_cart_clear(request):
    """API endpoint for clearing the entire cart."""
    request.session['cart'] = []
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': 'Cart cleared successfully',
        'cart_count': 0
    })


# =============================================================================
# CHECKOUT
# =============================================================================

@login_required
@require_POST
def checkout(request):
    """Process checkout."""
    cart = request.session.get('cart', [])
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not cart:
        if is_ajax:
            return JsonResponse({'success': False, 'message': 'Your cart is empty'})
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
        if is_ajax:
            return JsonResponse({'success': False, 'message': 'Customer profile not found'})
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
        if is_ajax:
            from django.urls import reverse
            return JsonResponse({
                'success': True,
                'message': 'Order placed successfully!',
                'redirect': reverse('order_detail', args=[result['order_id']])
            })
        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', order_id=result['order_id'])
    else:
        if is_ajax:
            return JsonResponse({'success': False, 'message': result['message']})
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


@customer_required
@require_POST
def api_order_cancel(request):
    """API endpoint for cancelling an order."""
    import json
    
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found'})
    
    # Verify order belongs to customer
    customer_id = Auth.get_customer_id(request)
    if order.customer_id != customer_id:
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    if order.status != 'pending':
        return JsonResponse({'success': False, 'message': 'Only pending orders can be cancelled'})
    
    result = order.cancel_order()
    
    return JsonResponse(result)


# =============================================================================
# ACCOUNT
# =============================================================================

@customer_required
def account(request):
    """View account details."""
    from django.db.models import Sum, Count
    
    customer_id = Auth.get_customer_id(request)

    if customer_id:
        try:
            customer = Customer.objects.select_related('user').get(id=customer_id)
            
            # Get customer stats
            stats = Order.objects.filter(customer_id=customer_id).aggregate(
                total_orders=Count('id'),
                total_spent=Sum('total')
            )
            stats['total_orders'] = stats['total_orders'] or 0
            stats['total_spent'] = stats['total_spent'] or 0
        except Customer.DoesNotExist:
            customer = None
            stats = {'total_orders': 0, 'total_spent': 0}
    else:
        customer = None
        stats = {'total_orders': 0, 'total_spent': 0}

    return render(request, 'customer/account.html', {
        'customer': customer,
        'stats': stats,
        'role': request.user.role,
    })


@customer_required
@require_POST
def account_update(request):
    """Update account details."""
    customer_id = Auth.get_customer_id(request)

    if not customer_id:
        return JsonResponse({'success': False, 'message': 'Customer profile not found'})

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Customer profile not found'})

    # Update customer details
    customer.first_name = request.POST.get('first_name', customer.first_name)
    customer.last_name = request.POST.get('last_name', customer.last_name)
    customer.phone = request.POST.get('phone', customer.phone)
    customer.address = request.POST.get('address', customer.address)
    customer.city = request.POST.get('city', getattr(customer, 'city', ''))
    customer.state = request.POST.get('state', getattr(customer, 'state', ''))
    customer.zip_code = request.POST.get('zip_code', getattr(customer, 'zip_code', ''))

    # Update email if provided
    email = request.POST.get('email')
    if email and email != request.user.email:
        request.user.email = email
        request.user.save()

    try:
        customer.save()
        return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to update account: {str(e)}'})


@customer_required
@require_POST
def change_password(request):
    """Change user password."""
    from django.contrib.auth.hashers import check_password, make_password
    
    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '')
    confirm_password = request.POST.get('confirm_password', '')
    
    # Validate inputs
    if not current_password or not new_password or not confirm_password:
        return JsonResponse({'success': False, 'message': 'All password fields are required'})
    
    if new_password != confirm_password:
        return JsonResponse({'success': False, 'message': 'New passwords do not match'})
    
    if len(new_password) < 6:
        return JsonResponse({'success': False, 'message': 'Password must be at least 6 characters'})
    
    # Verify current password
    user = request.user
    if not check_password(current_password, user.password):
        return JsonResponse({'success': False, 'message': 'Current password is incorrect'})
    
    # Update password
    try:
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({'success': True, 'message': 'Password updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Failed to update password: {str(e)}'})


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
    path('api/cart/update/', api_cart_update, name='api_cart_update'),
    path('api/cart/remove/', api_cart_remove, name='api_cart_remove'),
    path('api/cart/clear/', api_cart_clear, name='api_cart_clear'),

    # Checkout
    path('checkout/', checkout, name='checkout'),
    path('checkout/', checkout, name='customer_checkout'),

    # Order cancellation
    path('orders/<int:order_id>/cancel/', order_cancel, name='order_cancel'),
    path('orders/<int:order_id>/cancel/', order_cancel, name='customer_order_cancel'),
    
    # Order API
    path('api/order/cancel/', api_order_cancel, name='api_order_cancel'),

    # Account
    path('account/', account, name='account'),
    path('account/', account, name='customer_account'),
    path('account/update/', account_update, name='account_update'),
    path('account/update/', account_update, name='customer_account_update'),
    path('account/change-password/', change_password, name='change_password'),
    path('account/delete/', account_delete, name='account_delete'),
    path('account/delete/', account_delete, name='customer_account_delete'),
]
