"""
Reports View
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
    """Display reports page"""
    
    # Only accessible to staff/admin
    if st.session_state.role not in ['admin', 'staff']:
        st.error("Access denied. This page is for staff only.")
        return
    
    st.title("📊 Reports & Analytics")
    
    tabs = st.tabs(["Sales Report", "Product Performance", "Customer Insights", "Inventory Report"])
    
    with tabs[0]:
        show_sales_report()
    
    with tabs[1]:
        show_product_performance()
    
    with tabs[2]:
        show_customer_insights()
    
    with tabs[3]:
        show_inventory_report()

def show_sales_report():
    """Show sales analytics"""
    st.subheader("💰 Sales Report")
    
    order_model = OrderModel()
    
    # Get all orders
    orders = order_model.get_all_orders()
    
    if not orders:
        st.info("No sales data available")
        return
    
    df = pd.DataFrame(orders)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Summary metrics
    total_revenue = df[df['status'] != 'Cancelled']['total'].sum()
    total_orders = len(df)
    avg_order = total_revenue / len(df[df['status'] != 'Cancelled']) if len(df[df['status'] != 'Cancelled']) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", format_currency(total_revenue))
    with col2:
        st.metric("Total Orders", total_orders)
    with col3:
        st.metric("Average Order Value", format_currency(avg_order))
    
    st.divider()
    
    # Revenue over time
    st.subheader("Revenue Trend")
    df_valid = df[df['status'] != 'Cancelled'].copy()
    df_valid['date'] = df_valid['order_date'].dt.date
    daily_revenue = df_valid.groupby('date')['total'].sum().reset_index()
    
    fig = px.line(daily_revenue, x='date', y='total', 
                  labels={'date': 'Date', 'total': 'Revenue'},
                  title='Daily Revenue')
    fig.update_traces(line_color='#2E86AB')
    st.plotly_chart(fig, use_container_width=True)
    
    # Orders by status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Orders by Status")
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    color_discrete_sequence=['#2E86AB', '#A23B72', '#06A77D', '#F18F01', '#C73E1D', '#6C757D'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Payment Method")
        payment_revenue = df_valid.groupby('payment_method')['total'].sum().reset_index()
        fig = px.bar(payment_revenue, x='payment_method', y='total',
                    color='payment_method',
                    labels={'payment_method': 'Payment Method', 'total': 'Revenue'},
                    color_discrete_sequence=['#2E86AB', '#A23B72', '#06A77D', '#F18F01'])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def show_product_performance():
    """Show product performance analytics"""
    st.subheader("📦 Product Performance")
    
    order_model = OrderModel()
    product_model = ProductModel()
    
    conn = order_model.get_connection()
    cursor = conn.cursor()
    
    # Top selling products
    cursor.execute('''
        SELECT p.name, p.sku, p.category, 
               SUM(oi.quantity) as units_sold,
               SUM(oi.subtotal) as revenue,
               COUNT(DISTINCT oi.order_id) as num_orders
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY oi.product_id
        ORDER BY revenue DESC
        LIMIT 20
    ''')
    top_products = cursor.fetchall()
    
    if top_products:
        st.subheader("Top 20 Products by Revenue")
        df_top = pd.DataFrame(top_products, 
                             columns=['Product', 'SKU', 'Category', 'Units Sold', 'Revenue', 'Orders'])
        df_top['Revenue'] = df_top['Revenue'].apply(format_currency)
        st.dataframe(df_top, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Revenue by category
        cursor.execute('''
            SELECT p.category, SUM(oi.subtotal) as revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY p.category
            ORDER BY revenue DESC
        ''')
        category_revenue = cursor.fetchall()
        
        if category_revenue:
            st.subheader("Revenue by Category")
            df_cat = pd.DataFrame(category_revenue, columns=['Category', 'Revenue'])
            
            fig = px.bar(df_cat, x='Category', y='Revenue',
                        color='Category',
                        color_discrete_sequence=['#2E86AB', '#A23B72', '#06A77D', '#F18F01', '#C73E1D', '#6C757D'])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No product sales data available")
    
    conn.close()
    
    # Low stock alert
    st.divider()
    st.subheader("⚠️ Low Stock Alert")
    low_stock = product_model.get_low_stock_products()
    
    if low_stock:
        df_low = pd.DataFrame(low_stock)
        df_low['price'] = df_low['price'].apply(format_currency)
        
        display_cols = ['name', 'sku', 'category', 'stock_quantity', 'reorder_level', 'price']
        df_display = df_low[display_cols]
        df_display.columns = ['Product', 'SKU', 'Category', 'Current Stock', 'Reorder Level', 'Price']
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.success("All products are well-stocked!")

def show_customer_insights():
    """Show customer analytics"""
    st.subheader("👥 Customer Insights")
    
    customer_model = CustomerModel()
    order_model = OrderModel()
    
    # Top customers
    top_customers = customer_model.get_top_customers(10)
    
    if top_customers:
        st.subheader("Top 10 Customers")
        df_top = pd.DataFrame(top_customers)
        
        # Handle None values
        df_top['total_spent'] = df_top['total_spent'].fillna(0)
        df_top['order_count'] = df_top['order_count'].fillna(0)
        
        df_top['total_spent_formatted'] = df_top['total_spent'].apply(format_currency)
        
        display_cols = ['first_name', 'last_name', 'email', 'order_count', 'total_spent_formatted']
        available_cols = [col for col in display_cols if col in df_top.columns]
        
        if available_cols:
            df_display = df_top[available_cols]
            df_display.columns = ['First Name', 'Last Name', 'Email', 'Total Orders', 'Total Spent']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Customer distribution chart
        st.subheader("Customer Spending Distribution")
        fig = px.bar(df_top[:10], x='first_name', y='total_spent',
                    labels={'first_name': 'Customer', 'total_spent': 'Total Spent'},
                    color='total_spent',
                    color_continuous_scale=['#2E86AB', '#A23B72'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No customer data available")
    
    # Customer statistics
    conn = customer_model.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM customers')
    total_customers = cursor.fetchone()['total']
    
    cursor.execute('''
        SELECT COUNT(DISTINCT customer_id) as active 
        FROM orders 
        WHERE order_date >= datetime('now', '-30 days')
    ''')
    active_customers = cursor.fetchone()['active']
    
    conn.close()
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Customers", total_customers)
    
    with col2:
        st.metric("Active (Last 30 Days)", active_customers)

def show_inventory_report():
    """Show inventory analytics"""
    st.subheader("📦 Inventory Report")
    
    product_model = ProductModel()
    
    products = product_model.get_all_products(active_only=False)
    
    if not products:
        st.info("No inventory data available")
        return
    
    df = pd.DataFrame(products)
    
    # Summary metrics
    total_products = len(df)
    total_value = (df['stock_quantity'] * df['price']).sum()
    total_cost = (df['stock_quantity'] * df['cost']).sum()
    active_products = len(df[df['is_active'] == 1])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", total_products)
    
    with col2:
        st.metric("Active Products", active_products)
    
    with col3:
        st.metric("Inventory Value", format_currency(total_value))
    
    with col4:
        potential_profit = total_value - total_cost
        st.metric("Potential Profit", format_currency(potential_profit))
    
    st.divider()
    
    # Stock by category
    st.subheader("Stock by Category")
    category_stock = df.groupby('category').agg({
        'stock_quantity': 'sum',
        'price': lambda x: (df.loc[x.index, 'stock_quantity'] * x).sum()
    }).reset_index()
    category_stock.columns = ['Category', 'Total Units', 'Total Value']
    
    fig = px.bar(category_stock, x='Category', y='Total Value',
                color='Category',
                color_discrete_sequence=['#2E86AB', '#A23B72', '#06A77D', '#F18F01', '#C73E1D', '#6C757D'])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Stock levels
    st.divider()
    st.subheader("Stock Level Distribution")
    
    low_stock = len(df[df['stock_quantity'] <= df['reorder_level']])
    good_stock = len(df[df['stock_quantity'] > df['reorder_level']])
    out_of_stock = len(df[df['stock_quantity'] == 0])
    
    stock_dist = pd.DataFrame({
        'Status': ['Out of Stock', 'Low Stock', 'In Stock'],
        'Count': [out_of_stock, low_stock - out_of_stock, good_stock]
    })
    
    fig = px.pie(stock_dist, values='Count', names='Status',
                color_discrete_sequence=['#C73E1D', '#F18F01', '#06A77D'])
    st.plotly_chart(fig, use_container_width=True)
