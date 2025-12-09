"""
ShopPy - Authentication Module
Handles login, logout, registration, and authorization.
Equivalent to Perl ECommerce::Controllers::Auth
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lib.ECommerce.Models.User import User
from lib.ECommerce.Models.Customer import Customer


class Auth:
    """Authentication controller for ShopPy."""

    @staticmethod
    def login_user(request, username, password):
        """
        Authenticate and login a user.
        Returns user object on success, None on failure.
        """
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)

            # Store customer_id in session if user is a customer
            if user.role == 'customer':
                customer = Customer.get_customer_by_user_id(user.id)
                if customer:
                    request.session['customer_id'] = customer.id

            return user
        return None

    @staticmethod
    def logout_user(request):
        """Logout the current user."""
        logout(request)
        # Clear session data
        request.session.flush()

    @staticmethod
    def register_user(username, email, password, role='customer',
                      first_name='', last_name='', phone='', address=''):
        """
        Register a new user.
        Returns dict with success status and message/user_id.
        """
        # Validate input
        if not username:
            return {'success': False, 'message': 'Username is required'}
        if not email:
            return {'success': False, 'message': 'Email is required'}
        if not password:
            return {'success': False, 'message': 'Password is required'}
        if len(password) < 6:
            return {'success': False, 'message': 'Password must be at least 6 characters'}

        # Check if username exists
        if User.objects.filter(username=username).exists():
            return {'success': False, 'message': 'Username already exists'}

        # Check if email exists
        if User.objects.filter(email=email).exists():
            return {'success': False, 'message': 'Email address already registered'}

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )

            # If customer role, create customer profile
            if role == 'customer':
                Customer.objects.create(
                    user=user,
                    first_name=first_name or username,
                    last_name=last_name,
                    phone=phone,
                    address=address
                )

            return {'success': True, 'user_id': user.id}

        except Exception as e:
            return {'success': False, 'message': f'Failed to create user: {str(e)}'}

    @staticmethod
    def is_admin(user):
        """Check if user has admin role."""
        return user.is_authenticated and user.role == 'admin'

    @staticmethod
    def is_staff(user):
        """Check if user has staff or admin role."""
        return user.is_authenticated and user.role in ['staff', 'admin']

    @staticmethod
    def is_customer(user):
        """Check if user has customer role."""
        return user.is_authenticated and user.role == 'customer'

    @staticmethod
    def get_customer_id(request):
        """Get customer ID from session or user."""
        # First check session
        customer_id = request.session.get('customer_id')
        if customer_id:
            return customer_id

        # Then check user's customer profile
        if request.user.is_authenticated and request.user.role == 'customer':
            customer = Customer.get_customer_by_user_id(request.user.id)
            if customer:
                request.session['customer_id'] = customer.id
                return customer.id

        return None
