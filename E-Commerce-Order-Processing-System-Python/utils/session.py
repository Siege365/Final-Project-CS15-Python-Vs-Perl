"""
Session State Management Utilities
"""

import streamlit as st

def init_session_state():
    """Initialize session state variables"""
    
    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'email' not in st.session_state:
        st.session_state.email = None
    
    if 'role' not in st.session_state:
        st.session_state.role = None
    
    if 'customer_id' not in st.session_state:
        st.session_state.customer_id = None
    
    # Shopping cart
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'

def add_to_cart(product_id, product_name, price, quantity=1):
    """Add item to cart"""
    # Check if product already in cart
    for item in st.session_state.cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            return
    
    # Add new item
    st.session_state.cart.append({
        'product_id': product_id,
        'product_name': product_name,
        'unit_price': price,
        'quantity': quantity,
        'subtotal': price * quantity
    })

def remove_from_cart(product_id):
    """Remove item from cart"""
    st.session_state.cart = [
        item for item in st.session_state.cart 
        if item['product_id'] != product_id
    ]

def update_cart_quantity(product_id, quantity):
    """Update quantity of item in cart"""
    for item in st.session_state.cart:
        if item['product_id'] == product_id:
            item['quantity'] = quantity
            item['subtotal'] = item['unit_price'] * quantity
            break

def clear_cart():
    """Clear all items from cart"""
    st.session_state.cart = []

def get_cart_total():
    """Calculate cart total"""
    return sum(item['subtotal'] for item in st.session_state.cart)

def get_cart_count():
    """Get total items in cart"""
    return sum(item['quantity'] for item in st.session_state.cart)
