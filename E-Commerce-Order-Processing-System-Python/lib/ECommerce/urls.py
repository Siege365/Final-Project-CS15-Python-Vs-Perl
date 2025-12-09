"""
ShopPy - URL Configuration
Main URL routing for the e-commerce application.
Equivalent to Perl routes/ folder
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import route modules
from lib.ECommerce.Controllers import shared_routes, admin_routes, customer_routes

urlpatterns = [
    # Shared routes (accessible by all authenticated users)
    path('', include(shared_routes)),

    # Admin routes (admin/staff only)
    path('', include(admin_routes)),

    # Customer routes (customer only)
    path('', include(customer_routes)),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
