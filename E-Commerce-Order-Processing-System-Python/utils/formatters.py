"""
Formatting Utility Functions
"""

from datetime import datetime
from config.config import APP_CONFIG

def format_currency(amount):
    """Format number as currency"""
    symbol = APP_CONFIG['currency_symbol']
    return f"{symbol}{amount:,.2f}"

def format_date(date_str):
    """Format date string"""
    if not date_str:
        return "N/A"
    
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = date_str
        return dt.strftime("%B %d, %Y")
    except:
        return date_str

def format_datetime(date_str):
    """Format datetime string"""
    if not date_str:
        return "N/A"
    
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = date_str
        return dt.strftime("%B %d, %Y %I:%M %p")
    except:
        return date_str

def format_phone(phone):
    """Format phone number"""
    if not phone:
        return "N/A"
    
    # Remove non-numeric characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def get_status_color(status):
    """Get color for order status"""
    colors = {
        'Pending': 'warning',
        'Processing': 'info',
        'Shipped': 'primary',
        'Delivered': 'success',
        'Cancelled': 'error',
        'Refunded': 'secondary'
    }
    return colors.get(status, 'info')

def calculate_tax(subtotal, tax_rate=None):
    """Calculate tax amount"""
    if tax_rate is None:
        tax_rate = APP_CONFIG['tax_rate']
    return subtotal * tax_rate

def calculate_shipping(subtotal, shipping_cost=None, free_threshold=None):
    """Calculate shipping cost"""
    if shipping_cost is None:
        shipping_cost = APP_CONFIG['shipping_cost']
    if free_threshold is None:
        free_threshold = APP_CONFIG['free_shipping_threshold']
    
    return 0 if subtotal >= free_threshold else shipping_cost

def truncate_text(text, max_length=50):
    """Truncate text to max length"""
    if not text:
        return ""
    return text[:max_length] + "..." if len(text) > max_length else text
