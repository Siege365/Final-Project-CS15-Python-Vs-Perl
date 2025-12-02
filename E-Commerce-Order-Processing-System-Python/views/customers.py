"""
Customers View
"""

import streamlit as st
import pandas as pd
from models.customer import CustomerModel
from models.order import OrderModel
from utils.formatters import format_currency, format_date, format_phone

def show():
    """Display customers page"""
    
    # Only accessible to staff/admin
    if st.session_state.role not in ['admin', 'staff']:
        st.error("Access denied. This page is for staff only.")
        return
    
    st.title("👥 Customer Management")
    
    customer_model = CustomerModel()
    
    tabs = st.tabs(["All Customers", "Add Customer", "Customer Details", "Top Customers"])
    
    with tabs[0]:
        show_all_customers(customer_model)
    
    with tabs[1]:
        show_add_customer(customer_model)
    
    with tabs[2]:
        show_customer_details(customer_model)
    
    with tabs[3]:
        show_top_customers(customer_model)

def show_all_customers(customer_model):
    """Show all customers table"""
    st.subheader("All Customers")
    
    # Search
    search_term = st.text_input("🔍 Search customers", placeholder="Search by name, phone, or email...")
    
    # Get customers
    if search_term:
        customers = customer_model.search_customers(search_term)
    else:
        customers = customer_model.get_all_customers()
    
    if customers:
        df = pd.DataFrame(customers)
        
        # Format phone numbers
        if 'phone' in df.columns:
            df['phone'] = df['phone'].apply(lambda x: format_phone(x) if x else 'N/A')
        
        display_cols = ['id', 'first_name', 'last_name', 'phone', 'email', 'city', 'state']
        available_cols = [col for col in display_cols if col in df.columns]
        
        if available_cols:
            df_display = df[available_cols]
            df_display.columns = [col.replace('_', ' ').title() for col in available_cols]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.info(f"Total customers: {len(customers)}")
    else:
        st.info("No customers found")

def show_add_customer(customer_model):
    """Show add customer form"""
    st.subheader("Add New Customer")
    
    with st.form("add_customer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            phone = st.text_input("Phone*")
            email = st.text_input("Email")
        
        with col2:
            address = st.text_input("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            zip_code = st.text_input("ZIP Code")
        
        submit = st.form_submit_button("Add Customer", use_container_width=True)
        
        if submit:
            if not all([first_name, last_name, phone]):
                st.error("Please fill in all required fields (*)")
            else:
                try:
                    customer_id = customer_model.create_customer(
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        address=address,
                        city=city,
                        state=state,
                        zip_code=zip_code
                    )
                    st.success(f"Customer '{first_name} {last_name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding customer: {str(e)}")

def show_customer_details(customer_model):
    """Show customer details and edit form"""
    st.subheader("Customer Details")
    
    customers = customer_model.get_all_customers()
    
    if customers:
        customer_id = st.selectbox("Select Customer",
                                  options=[c['id'] for c in customers],
                                  format_func=lambda x: f"{next(c['first_name'] for c in customers if c['id'] == x)} {next(c['last_name'] for c in customers if c['id'] == x)}")
        
        if customer_id:
            customer = customer_model.get_customer_by_id(customer_id)
            
            # Customer stats
            stats = customer_model.get_customer_stats(customer_id)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Orders", stats['total_orders'])
            
            with col2:
                st.metric("Total Spent", format_currency(stats['total_spent']))
            
            with col3:
                st.metric("Avg Order Value", format_currency(stats['avg_order_value']))
            
            with col4:
                st.metric("Last Order", format_date(stats['last_order']) if stats['last_order'] else 'Never')
            
            st.divider()
            
            # Edit form
            st.subheader("Edit Customer Information")
            
            with st.form("edit_customer_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name", value=customer['first_name'] or '')
                    last_name = st.text_input("Last Name", value=customer['last_name'] or '')
                    phone = st.text_input("Phone", value=customer['phone'] or '')
                    email = st.text_input("Email", value=customer.get('email') or '')
                
                with col2:
                    address = st.text_input("Address", value=customer['address'] or '')
                    city = st.text_input("City", value=customer['city'] or '')
                    state = st.text_input("State", value=customer['state'] or '')
                    zip_code = st.text_input("ZIP Code", value=customer['zip_code'] or '')
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Update Customer", use_container_width=True)
                with col2:
                    delete = st.form_submit_button("Delete Customer", use_container_width=True)
                
                if submit:
                    customer_model.update_customer(
                        customer_id,
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        address=address,
                        city=city,
                        state=state,
                        zip_code=zip_code
                    )
                    st.success("Customer updated successfully!")
                    st.rerun()
                
                if delete:
                    customer_model.delete_customer(customer_id)
                    st.success("Customer deleted!")
                    st.rerun()
            
            # Order history
            st.divider()
            st.subheader("Order History")
            
            order_model = OrderModel()
            orders = order_model.get_orders_by_customer(customer_id)
            
            if orders:
                df_orders = pd.DataFrame(orders)
                df_orders['total'] = df_orders['total'].apply(format_currency)
                df_orders['order_date'] = df_orders['order_date'].apply(format_date)
                
                display_cols = ['order_number', 'order_date', 'status', 'total']
                df_display = df_orders[display_cols]
                df_display.columns = ['Order #', 'Date', 'Status', 'Total']
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.info("No orders yet")
    else:
        st.info("No customers found")

def show_top_customers(customer_model):
    """Show top customers by spending"""
    st.subheader("🏆 Top Customers")
    
    limit = st.slider("Show top customers", min_value=5, max_value=50, value=10, step=5)
    
    top_customers = customer_model.get_top_customers(limit)
    
    if top_customers:
        df = pd.DataFrame(top_customers)
        
        # Handle None values
        df['total_spent'] = df['total_spent'].fillna(0)
        df['order_count'] = df['order_count'].fillna(0)
        
        df['total_spent_formatted'] = df['total_spent'].apply(format_currency)
        df['phone_formatted'] = df['phone'].apply(format_phone)
        
        display_cols = ['first_name', 'last_name', 'phone_formatted', 'email', 'order_count', 'total_spent_formatted']
        available_cols = [col for col in display_cols if col in df.columns]
        
        if available_cols:
            df_display = df[available_cols]
            df_display.columns = ['First Name', 'Last Name', 'Phone', 'Email', 'Orders', 'Total Spent']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No customer data available")
