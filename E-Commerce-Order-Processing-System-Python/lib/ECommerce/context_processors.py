"""
ShopPy - Context Processors
Provides common context variables to all templates.
"""

from lib.ECommerce.Config import APP_CONFIG


def cart_context(request):
    """Add cart information to template context."""
    cart = request.session.get('cart', [])
    cart_count = len(cart)  # Number of distinct products

    return {
        'cart': cart,
        'cart_count': cart_count,
    }


def app_config(request):
    """Add application configuration to template context."""
    return {
        'app_config': APP_CONFIG,
        'APP_NAME': APP_CONFIG['app_name'],
        'APP_SLOGAN': APP_CONFIG['slogan'],
    }
