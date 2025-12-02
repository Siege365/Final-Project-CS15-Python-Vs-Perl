"""
Dashboard View
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from models.order import OrderModel
from models.product import ProductModel
from models.customer import CustomerModel
from utils.formatters import format_currency, format_date

def show():
    """Display dashboard"""
    st.title("📊 Dashboard")
    
    order_model = OrderModel()
    product_model = ProductModel()
    customer_model = CustomerModel()
    
    # Get statistics
    order_stats = order_model.get_order_stats()
    products = product_model.get_all_products()
    low_stock = product_model.get_low_stock_products()
    recent_orders = order_model.get_recent_orders(10)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(order_stats["total_revenue"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Revenue</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{order_stats["total_orders"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Orders</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(products)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Products</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(order_stats["avg_order_value"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg Order Value</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Orders by Status")
        if order_stats['status_counts']:
            df_status = pd.DataFrame(list(order_stats['status_counts'].items()), 
                                    columns=['Status', 'Count'])
            fig = px.pie(df_status, values='Count', names='Status', 
                        color_discrete_sequence=['#2E86AB', '#A23B72', '#06A77D', '#F18F01', '#C73E1D', '#6C757D'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No orders yet")
    
    with col2:
        st.subheader("💰 Revenue by Payment Method")
        if recent_orders:
            # Group by payment method
            payment_totals = {}
            for order in recent_orders:
                method = order.get('payment_method', 'Unknown')
                payment_totals[method] = payment_totals.get(method, 0) + order.get('total', 0)
            
            if payment_totals:
                df_payment = pd.DataFrame(list(payment_totals.items()), 
                                         columns=['Payment Method', 'Total'])
                fig = px.bar(df_payment, x='Payment Method', y='Total',
                           color='Payment Method',
                           color_discrete_sequence=['#2E86AB', '#A23B72', '#06A77D', '#F18F01'])
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order data available")
    
    st.divider()
    
    # Recent orders and low stock
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛒 Recent Orders")
        if recent_orders:
            for order in recent_orders[:5]:
                with st.container():
                    st.markdown(f"""
                    **{order['order_number']}** - {format_currency(order['total'])}  
                    Customer: {order.get('first_name', 'N/A')} {order.get('last_name', '')}  
                    Status: `{order['status']}`  
                    Date: {format_date(order['order_date'])}
                    """)
                    st.divider()
        else:
            st.info("No orders yet")
    
    with col2:
        st.subheader("⚠️ Low Stock Alert")
        if low_stock:
            for product in low_stock[:5]:
                with st.container():
                    st.markdown(f"""
                    **{product['name']}** (SKU: {product['sku']})  
                    Stock: `{product['stock_quantity']}` units  
                    Reorder Level: {product['reorder_level']}  
                    Price: {format_currency(product['price'])}
                    """)
                    st.divider()
        else:
            st.success("All products are well-stocked!")
    
    # Top products (if staff/admin)
    if st.session_state.role in ['admin', 'staff']:
        st.divider()
        st.subheader("🏆 Top Selling Products")
        
        # Get top products from order items
        conn = order_model.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.name, p.sku, SUM(oi.quantity) as total_sold, 
                   SUM(oi.subtotal) as revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY oi.product_id
            ORDER BY total_sold DESC
            LIMIT 5
        ''')
        top_products = cursor.fetchall()
        conn.close()
        
        if top_products:
            df_top = pd.DataFrame(top_products, columns=['Product', 'SKU', 'Units Sold', 'Revenue'])
            df_top['Revenue'] = df_top['Revenue'].apply(format_currency)
            st.dataframe(df_top, use_container_width=True, hide_index=True)
        else:
            st.info("No sales data available yet")
