"""
Orders View
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from models.order import OrderModel
from models.product import ProductModel
from models.customer import CustomerModel
from utils.formatters import format_currency, format_date, format_datetime, get_status_color
from utils.session import get_cart_total, get_cart_count, clear_cart, remove_from_cart, update_cart_quantity
from config.config import ORDER_STATUS, PAYMENT_METHODS, APP_CONFIG

def show():
    """Display orders page"""
    order_model = OrderModel()
    
    is_staff = st.session_state.role in ['admin', 'staff']
    
    if is_staff:
        show_order_management(order_model)
    else:
        show_customer_orders(order_model)

def show_customer_orders(order_model):
    """Show customer's orders and shopping cart"""
    st.title("🛒 My Orders")
    
    tabs = st.tabs(["Shopping Cart", "Order History"])
    
    with tabs[0]:
        show_shopping_cart()
    
    with tabs[1]:
        show_order_history(order_model)

def show_shopping_cart():
    """Show shopping cart and checkout"""
    st.subheader("Shopping Cart")
    
    cart = st.session_state.cart
    
    if not cart:
        st.info("Your cart is empty. Browse products to add items!")
        return
    
    # Display cart items
    for i, item in enumerate(cart):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{item['product_name']}**")
        
        with col2:
            st.write(format_currency(item['unit_price']))
        
        with col3:
            new_qty = st.number_input("Qty", min_value=1, value=item['quantity'], 
                                     key=f"cart_qty_{i}", label_visibility="collapsed")
            if new_qty != item['quantity']:
                update_cart_quantity(item['product_id'], new_qty)
                st.rerun()
        
        with col4:
            st.write(format_currency(item['subtotal']))
        
        with col5:
            if st.button("🗑️", key=f"remove_{i}"):
                remove_from_cart(item['product_id'])
                st.rerun()
    
    st.divider()
    
    # Cart summary
    subtotal = get_cart_total()
    tax = subtotal * APP_CONFIG['tax_rate']
    shipping = 0 if subtotal >= APP_CONFIG['free_shipping_threshold'] else APP_CONFIG['shipping_cost']
    total = subtotal + tax + shipping
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### Order Summary")
        st.write(f"Subtotal: {format_currency(subtotal)}")
        st.write(f"Tax ({APP_CONFIG['tax_rate']*100}%): {format_currency(tax)}")
        st.write(f"Shipping: {format_currency(shipping)}")
        if shipping == 0:
            st.success("Free shipping!")
        st.markdown(f"### Total: {format_currency(total)}")
    
    st.divider()
    
    # Checkout form
    st.subheader("Checkout")
    
    with st.form("checkout_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Shipping Information**")
            ship_address = st.text_input("Address*")
            ship_city = st.text_input("City*")
        
        with col2:
            st.write("**Payment**")
            ship_state = st.text_input("State*")
            ship_zip = st.text_input("ZIP Code*")
        
        payment_method = st.selectbox("Payment Method*", PAYMENT_METHODS)
        notes = st.text_area("Order Notes (optional)")
        
        submit = st.form_submit_button("Place Order", use_container_width=True)
        
        if submit:
            if not all([ship_address, ship_city, ship_state, ship_zip]):
                st.error("Please fill in all required fields")
            else:
                # Create order
                try:
                    order_model = OrderModel()
                    customer_model = CustomerModel()
                    
                    # Get or create customer
                    customer = customer_model.get_customer_by_user_id(st.session_state.user_id)
                    if not customer:
                        customer_id = customer_model.create_customer(
                            first_name=st.session_state.username,
                            last_name='',
                            phone='',
                            email=st.session_state.email,
                            user_id=st.session_state.user_id
                        )
                    else:
                        customer_id = customer['id']
                    
                    order_id, order_number = order_model.create_order(
                        customer_id=customer_id,
                        items=cart,
                        payment_method=payment_method,
                        subtotal=subtotal,
                        tax=tax,
                        shipping_cost=shipping,
                        total=total,
                        shipping_address=ship_address,
                        shipping_city=ship_city,
                        shipping_state=ship_state,
                        shipping_zip=ship_zip,
                        notes=notes,
                        created_by=st.session_state.user_id
                    )
                    
                    clear_cart()
                    st.success(f"Order placed successfully! Order #: {order_number}")
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error placing order: {str(e)}")

def show_order_history(order_model):
    """Show customer's order history"""
    st.subheader("Order History")
    
    # Get customer orders
    customer_model = CustomerModel()
    customer = customer_model.get_customer_by_user_id(st.session_state.user_id)
    
    if customer:
        orders = order_model.get_orders_by_customer(customer['id'])
        
        if orders:
            for order in orders:
                with st.expander(f"Order {order['order_number']} - {format_currency(order['total'])} - {order['status']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Date:** {format_datetime(order['order_date'])}")
                        st.write(f"**Status:** {order['status']}")
                        st.write(f"**Payment:** {order['payment_method']}")
                    
                    with col2:
                        st.write(f"**Subtotal:** {format_currency(order['subtotal'])}")
                        st.write(f"**Tax:** {format_currency(order['tax'])}")
                        st.write(f"**Shipping:** {format_currency(order['shipping_cost'])}")
                        st.write(f"**Total:** {format_currency(order['total'])}")
                    
                    # Order items
                    items = order_model.get_order_items(order['id'])
                    if items:
                        st.write("**Items:**")
                        for item in items:
                            st.write(f"- {item['product_name']} x {item['quantity']} @ {format_currency(item['unit_price'])} = {format_currency(item['subtotal'])}")
        else:
            st.info("No orders yet")
    else:
        st.info("No orders yet")

def show_order_management(order_model):
    """Show order management for staff/admin"""
    st.title("📦 Order Management")
    
    tabs = st.tabs(["All Orders", "Create Order", "Order Details"])
    
    with tabs[0]:
        show_all_orders(order_model)
    
    with tabs[1]:
        show_create_order(order_model)
    
    with tabs[2]:
        show_order_details(order_model)

def show_all_orders(order_model):
    """Show all orders table"""
    st.subheader("All Orders")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("Search orders")
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ['All'] + ORDER_STATUS)
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Date: Newest", "Date: Oldest", "Total: High to Low"])
    
    # Get orders
    if search_term:
        orders = order_model.search_orders(search_term)
    elif status_filter != 'All':
        orders = order_model.get_orders_by_status(status_filter)
    else:
        orders = order_model.get_all_orders()
    
    # Sort
    if sort_by == "Date: Oldest":
        orders = sorted(orders, key=lambda x: x['order_date'])
    elif sort_by == "Total: High to Low":
        orders = sorted(orders, key=lambda x: x['total'], reverse=True)
    
    if orders:
        # Display as table
        df = pd.DataFrame(orders)
        df['total'] = df['total'].apply(format_currency)
        df['order_date'] = df['order_date'].apply(format_datetime)
        
        display_cols = ['order_number', 'first_name', 'last_name', 'total', 'status', 'order_date']
        if all(col in df.columns for col in display_cols):
            df_display = df[display_cols]
            df_display.columns = ['Order #', 'First Name', 'Last Name', 'Total', 'Status', 'Date']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.info(f"Total orders: {len(orders)}")
    else:
        st.info("No orders found")

def show_create_order(order_model):
    """Show create order interface"""
    st.subheader("Create New Order")
    
    # This would be similar to customer checkout but with ability to select customer
    customer_model = CustomerModel()
    product_model = ProductModel()
    
    customers = customer_model.get_all_customers()
    products = product_model.get_all_products()
    
    with st.form("create_order_form"):
        # Customer selection
        customer_id = st.selectbox("Select Customer*",
                                  options=[c['id'] for c in customers],
                                  format_func=lambda x: f"{next(c['first_name'] for c in customers if c['id'] == x)} {next(c['last_name'] for c in customers if c['id'] == x)}")
        
        # Product selection
        st.write("**Add Products**")
        selected_products = st.multiselect("Select Products",
                                          options=[p['id'] for p in products],
                                          format_func=lambda x: f"{next(p['name'] for p in products if p['id'] == x)} - {format_currency(next(p['price'] for p in products if p['id'] == x))}")
        
        # Payment and shipping
        payment_method = st.selectbox("Payment Method*", PAYMENT_METHODS)
        
        submit = st.form_submit_button("Create Order")
        
        if submit and selected_products:
            st.info("Order creation functionality - quantities would be collected in a more detailed interface")

def show_order_details(order_model):
    """Show detailed order information"""
    st.subheader("Order Details")
    
    orders = order_model.get_all_orders()
    
    if orders:
        order_id = st.selectbox("Select Order",
                               options=[o['id'] for o in orders],
                               format_func=lambda x: next(o['order_number'] for o in orders if o['id'] == x))
        
        if order_id:
            order = order_model.get_order_by_id(order_id)
            items = order_model.get_order_items(order_id)
            
            # Order info
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Order Number:** {order['order_number']}")
                st.write(f"**Customer:** {order.get('first_name', 'N/A')} {order.get('last_name', '')}")
                st.write(f"**Phone:** {order.get('phone', 'N/A')}")
                st.write(f"**Date:** {format_datetime(order['order_date'])}")
            
            with col2:
                st.write(f"**Status:** {order['status']}")
                st.write(f"**Payment Method:** {order['payment_method']}")
                st.write(f"**Subtotal:** {format_currency(order['subtotal'])}")
                st.write(f"**Tax:** {format_currency(order['tax'])}")
                st.write(f"**Shipping:** {format_currency(order['shipping_cost'])}")
                st.write(f"**Total:** {format_currency(order['total'])}")
            
            # Shipping address
            if order.get('shipping_address'):
                st.write("**Shipping Address:**")
                st.write(f"{order['shipping_address']}, {order['shipping_city']}, {order['shipping_state']} {order['shipping_zip']}")
            
            # Order items
            if items:
                st.write("**Order Items:**")
                df_items = pd.DataFrame(items)
                df_items['unit_price'] = df_items['unit_price'].apply(format_currency)
                df_items['subtotal'] = df_items['subtotal'].apply(format_currency)
                
                display_cols = ['product_name', 'sku', 'quantity', 'unit_price', 'subtotal']
                df_display = df_items[display_cols]
                df_display.columns = ['Product', 'SKU', 'Quantity', 'Unit Price', 'Subtotal']
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Update status
            st.divider()
            col1, col2 = st.columns([1, 3])
            with col1:
                new_status = st.selectbox("Update Status", ORDER_STATUS, 
                                         index=ORDER_STATUS.index(order['status']) if order['status'] in ORDER_STATUS else 0)
            with col2:
                if st.button("Update Order Status"):
                    order_model.update_order_status(order_id, new_status)
                    st.success(f"Order status updated to {new_status}")
                    st.rerun()
    else:
        st.info("No orders yet")
