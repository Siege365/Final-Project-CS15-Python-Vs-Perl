"""
Products View
"""

import streamlit as st
import pandas as pd
from models.product import ProductModel
from utils.formatters import format_currency
from utils.session import add_to_cart, get_cart_count
from config.config import PRODUCT_CATEGORIES

def show():
    """Display products page"""
    product_model = ProductModel()
    
    # Check user role
    is_staff = st.session_state.role in ['admin', 'staff']
    
    if is_staff:
        show_product_management(product_model)
    else:
        show_product_catalog(product_model)

def show_product_catalog(product_model):
    """Show product catalog for customers"""
    st.title("🛍️ Product Catalog")
    
    # Cart indicator
    cart_count = get_cart_count()
    if cart_count > 0:
        st.success(f"🛒 Cart: {cart_count} items")
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search products", placeholder="Search by name, SKU, or description...")
    
    with col2:
        categories = ['All'] + product_model.get_categories()
        selected_category = st.selectbox("Category", categories)
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Price: Low to High", "Price: High to Low"])
    
    # Get products
    if search_term:
        products = product_model.search_products(search_term)
    elif selected_category != 'All':
        products = product_model.get_products_by_category(selected_category)
    else:
        products = product_model.get_all_products()
    
    # Sort products
    if sort_by == "Price: Low to High":
        products = sorted(products, key=lambda x: x['price'])
    elif sort_by == "Price: High to Low":
        products = sorted(products, key=lambda x: x['price'], reverse=True)
    else:
        products = sorted(products, key=lambda x: x['name'])
    
    st.divider()
    
    # Display products in grid
    if products:
        cols_per_row = 3
        for i in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(products):
                    product = products[i + j]
                    with col:
                        display_product_card(product, product_model)
    else:
        st.info("No products found")

def display_product_card(product, product_model):
    """Display a product card"""
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        st.subheader(product['name'])
        st.write(f"**SKU:** {product['sku']}")
        st.write(f"**Category:** {product['category']}")
        
        if product['description']:
            st.write(product['description'][:100] + "..." if len(product['description']) > 100 else product['description'])
        
        st.markdown(f"### {format_currency(product['price'])}")
        
        # Stock status
        stock = product['stock_quantity']
        if stock > 10:
            st.success(f"In Stock ({stock} available)")
        elif stock > 0:
            st.warning(f"Low Stock ({stock} available)")
        else:
            st.error("Out of Stock")
        
        # Add to cart
        if stock > 0:
            col1, col2 = st.columns([1, 2])
            with col1:
                quantity = st.number_input("Qty", min_value=1, max_value=stock, value=1, 
                                          key=f"qty_{product['id']}")
            with col2:
                if st.button("🛒 Add to Cart", key=f"add_{product['id']}", use_container_width=True):
                    add_to_cart(product['id'], product['name'], product['price'], quantity)
                    st.success(f"Added {quantity} to cart!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_product_management(product_model):
    """Show product management for staff/admin"""
    st.title("📦 Product Management")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["All Products", "Add Product", "Low Stock"])
    
    with tab1:
        show_all_products(product_model)
    
    with tab2:
        show_add_product(product_model)
    
    with tab3:
        show_low_stock(product_model)

def show_all_products(product_model):
    """Show all products table"""
    st.subheader("All Products")
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("Search products", key="search_all")
    with col2:
        show_inactive = st.checkbox("Show Inactive")
    
    # Get products
    if search_term:
        products = product_model.search_products(search_term)
    else:
        products = product_model.get_all_products(active_only=not show_inactive)
    
    if products:
        # Convert to DataFrame
        df = pd.DataFrame(products)
        df['price'] = df['price'].apply(format_currency)
        df['cost'] = df['cost'].apply(lambda x: format_currency(x) if x else 'N/A')
        
        # Select columns to display
        display_cols = ['id', 'name', 'sku', 'category', 'price', 'stock_quantity', 'is_active']
        df_display = df[display_cols]
        df_display.columns = ['ID', 'Name', 'SKU', 'Category', 'Price', 'Stock', 'Active']
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Edit/Delete options
        st.divider()
        st.subheader("Edit Product")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            product_id = st.selectbox("Select Product", 
                                     options=[p['id'] for p in products],
                                     format_func=lambda x: next(p['name'] for p in products if p['id'] == x))
        
        if product_id:
            product = product_model.get_product_by_id(product_id)
            show_edit_product(product, product_model)
    else:
        st.info("No products found")

def show_edit_product(product, product_model):
    """Show edit product form"""
    with st.form("edit_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Product Name", value=product['name'])
            sku = st.text_input("SKU", value=product['sku'])
            category = st.selectbox("Category", PRODUCT_CATEGORIES, 
                                   index=PRODUCT_CATEGORIES.index(product['category']) if product['category'] in PRODUCT_CATEGORIES else 0)
            price = st.number_input("Price", min_value=0.01, value=float(product['price']), step=0.01)
        
        with col2:
            cost = st.number_input("Cost", min_value=0.0, value=float(product['cost']) if product['cost'] else 0.0, step=0.01)
            stock = st.number_input("Stock Quantity", min_value=0, value=product['stock_quantity'])
            reorder_level = st.number_input("Reorder Level", min_value=0, value=product['reorder_level'])
            is_active = st.checkbox("Active", value=bool(product['is_active']))
        
        description = st.text_area("Description", value=product['description'] or '')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            submit = st.form_submit_button("Update Product", use_container_width=True)
        with col2:
            if st.form_submit_button("Delete Product", use_container_width=True):
                product_model.delete_product(product['id'])
                st.success("Product deleted!")
                st.rerun()
        
        if submit:
            product_model.update_product(
                product['id'],
                name=name,
                sku=sku,
                category=category,
                price=price,
                cost=cost,
                stock_quantity=stock,
                reorder_level=reorder_level,
                description=description,
                is_active=1 if is_active else 0
            )
            st.success("Product updated successfully!")
            st.rerun()

def show_add_product(product_model):
    """Show add product form"""
    st.subheader("Add New Product")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Product Name*")
            sku = st.text_input("SKU*")
            category = st.selectbox("Category*", PRODUCT_CATEGORIES)
            price = st.number_input("Price*", min_value=0.01, value=1.00, step=0.01)
        
        with col2:
            cost = st.number_input("Cost", min_value=0.0, value=0.0, step=0.01)
            stock = st.number_input("Stock Quantity", min_value=0, value=0)
            reorder_level = st.number_input("Reorder Level", min_value=0, value=10)
        
        description = st.text_area("Description")
        
        submit = st.form_submit_button("Add Product", use_container_width=True)
        
        if submit:
            if not all([name, sku, category, price]):
                st.error("Please fill in all required fields (*)")
            else:
                result = product_model.create_product(
                    name=name,
                    description=description,
                    category=category,
                    price=price,
                    cost=cost,
                    sku=sku,
                    stock_quantity=stock,
                    reorder_level=reorder_level
                )
                
                if result:
                    st.success(f"Product '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add product. SKU may already exist.")

def show_low_stock(product_model):
    """Show low stock products"""
    st.subheader("⚠️ Low Stock Products")
    
    low_stock = product_model.get_low_stock_products()
    
    if low_stock:
        df = pd.DataFrame(low_stock)
        df['price'] = df['price'].apply(format_currency)
        
        display_cols = ['name', 'sku', 'category', 'stock_quantity', 'reorder_level', 'price']
        df_display = df[display_cols]
        df_display.columns = ['Product', 'SKU', 'Category', 'Current Stock', 'Reorder Level', 'Price']
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.info(f"Total products below reorder level: {len(low_stock)}")
    else:
        st.success("All products are well-stocked!")
