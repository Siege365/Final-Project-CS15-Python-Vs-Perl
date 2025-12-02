"""
E-Commerce Order Processing System
Main Application Entry Point
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from controllers.auth import AuthController
from views import dashboard, products, orders, customers, reports, settings
from utils.session import init_session_state
from config.config import APP_CONFIG

# Page configuration
st.set_page_config(
    page_title="E-Commerce Order Processing System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('config/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    pass

# Initialize session state
init_session_state()

# Authentication controller
auth_controller = AuthController()

def main():
    """Main application logic"""
    
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    """Display login/registration page"""
    st.title("🛒 E-Commerce Order Processing System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("Login", use_container_width=True):
                    if auth_controller.login(login_username, login_password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            with col_btn2:
                if st.button("Demo Login (Admin)", use_container_width=True):
                    if auth_controller.login("admin", "admin123"):
                        st.success("Logged in as Admin!")
                        st.rerun()
    
    with tab2:
        st.subheader("Create New Account")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
            reg_role = st.selectbox("Account Type", ["customer", "staff"], key="reg_role")
            
            if st.button("Register", use_container_width=True):
                if not all([reg_username, reg_email, reg_password]):
                    st.error("Please fill in all fields")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    if auth_controller.register(reg_username, reg_email, reg_password, reg_role):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username already exists")

def show_main_app():
    """Display main application with navigation"""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🛒 E-Commerce System")
        st.write(f"**User:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role.upper()}")
        st.divider()
        
        # Navigation menu based on role
        if st.session_state.role in ['admin', 'staff']:
            page = st.radio(
                "Navigation",
                ["Dashboard", "Products", "Orders", "Customers", "Reports", "Settings"],
                key="nav_menu"
            )
        else:
            page = st.radio(
                "Navigation",
                ["Dashboard", "Products", "My Orders", "Settings"],
                key="nav_menu"
            )
        
        st.divider()
        
        if st.button("Logout", use_container_width=True):
            auth_controller.logout()
            st.rerun()
    
    # Route to appropriate page
    if page == "Dashboard":
        dashboard.show()
    elif page == "Products":
        products.show()
    elif page in ["Orders", "My Orders"]:
        orders.show()
    elif page == "Customers":
        customers.show()
    elif page == "Reports":
        reports.show()
    elif page == "Settings":
        settings.show()

if __name__ == "__main__":
    main()
