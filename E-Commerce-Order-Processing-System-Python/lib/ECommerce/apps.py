"""
ShopPy - E-Commerce App Configuration
"""

from django.apps import AppConfig


class ECommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lib.ECommerce'
    label = 'ECommerce'
    verbose_name = 'ShopPy E-Commerce'

    def ready(self):
        """Initialize the app when Django starts."""
        pass
