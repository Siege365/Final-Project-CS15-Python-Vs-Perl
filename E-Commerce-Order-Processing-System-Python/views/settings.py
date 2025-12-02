"""
Settings View
"""

import streamlit as st
from models.user import UserModel
from models.customer import CustomerModel

def show():
    """Display settings page"""
    st.title("⚙️ Settings")
    
    tabs = st.tabs(["Profile", "Account", "About"])
    
    with tabs[0]:
        show_profile()
    
    with tabs[1]:
        show_account()
    
    with tabs[2]:
        show_about()

def show_profile():
    """Show user profile settings"""
    st.subheader("Profile Settings")
    
    user_model = UserModel()
    customer_model = CustomerModel()
    
    user = user_model.get_user_by_id(st.session_state.user_id)
    
    if st.session_state.role == 'customer':
        customer = customer_model.get_customer_by_user_id(st.session_state.user_id)
        
        if customer:
            with st.form("profile_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name", value=customer['first_name'] or '')
                    last_name = st.text_input("Last Name", value=customer['last_name'] or '')
                    phone = st.text_input("Phone", value=customer['phone'] or '')
                
                with col2:
                    address = st.text_input("Address", value=customer['address'] or '')
                    city = st.text_input("City", value=customer['city'] or '')
                    state = st.text_input("State", value=customer['state'] or '')
                    zip_code = st.text_input("ZIP Code", value=customer['zip_code'] or '')
                
                submit = st.form_submit_button("Update Profile", use_container_width=True)
                
                if submit:
                    customer_model.update_customer(
                        customer['id'],
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        address=address,
                        city=city,
                        state=state,
                        zip_code=zip_code
                    )
                    st.success("Profile updated successfully!")
                    st.rerun()
        else:
            st.info("No profile information available")
    else:
        st.info("Profile management is available for customer accounts")

def show_account():
    """Show account settings"""
    st.subheader("Account Settings")
    
    user_model = UserModel()
    user = user_model.get_user_by_id(st.session_state.user_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Username:**", user['username'])
        st.write("**Email:**", user['email'])
        st.write("**Role:**", user['role'].upper())
    
    with col2:
        st.write("**Account Created:**", user['created_at'])
        st.write("**Last Login:**", user['last_login'] or 'N/A')
    
    st.divider()
    
    # Change password (placeholder - would need password hashing)
    st.subheader("Change Password")
    st.info("Password change functionality would be implemented here with proper security measures")

def show_about():
    """Show about page"""
    st.subheader("About E-Commerce Order Processing System")
    
    st.markdown("""
    ### 🛒 E-Commerce Order Processing System
    **Version:** 1.0.0
    
    A comprehensive order processing and inventory management system built with Python and Streamlit.
    
    #### Features:
    - 🔐 **User Authentication** - Role-based access control (Admin, Staff, Customer)
    - 📦 **Product Management** - Complete product catalog with inventory tracking
    - 🛍️ **Shopping Cart** - Customer shopping cart with checkout process
    - 📋 **Order Management** - Full order lifecycle management
    - 👥 **Customer Management** - Customer database and analytics
    - 📊 **Reports & Analytics** - Sales, product, and customer insights
    - 💾 **Database** - SQLite database with automated initialization
    
    #### Technology Stack:
    - **Framework:** Streamlit
    - **Database:** SQLite
    - **Charts:** Plotly
    - **Data Processing:** Pandas
    - **Security:** Bcrypt password hashing
    
    #### Default Login Credentials:
    - **Admin:** username: `admin`, password: `admin123`
    - **Staff:** username: `staff`, password: `staff123`
    - **Customer:** username: `customer`, password: `customer123`
    
    #### Support:
    For issues or questions, please contact your system administrator.
    
    ---
    
    © 2025 E-Commerce Order Processing System. All rights reserved.
    """)
    
    st.divider()
    
    # System statistics
    if st.session_state.role in ['admin', 'staff']:
        st.subheader("System Statistics")
        
        from models.order import OrderModel
        from models.product import ProductModel
        from models.customer import CustomerModel
        
        order_model = OrderModel()
        product_model = ProductModel()
        customer_model = CustomerModel()
        
        stats = order_model.get_order_stats()
        products = product_model.get_all_products()
        customers = customer_model.get_all_customers()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Orders", stats['total_orders'])
        
        with col2:
            st.metric("Total Products", len(products))
        
        with col3:
            st.metric("Total Customers", len(customers))
