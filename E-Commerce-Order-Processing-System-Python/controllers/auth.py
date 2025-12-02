"""
Authentication Controller
"""

import streamlit as st
from models.user import UserModel
from models.customer import CustomerModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.customer_model = CustomerModel()
    
    def login(self, username, password):
        """Authenticate user"""
        if self.user_model.verify_password(username, password):
            user = self.user_model.get_user_by_username(username)
            
            # Update last login
            self.user_model.update_last_login(user['id'])
            
            # Set session state
            st.session_state.logged_in = True
            st.session_state.user_id = user['id']
            st.session_state.username = user['username']
            st.session_state.email = user['email']
            st.session_state.role = user['role']
            
            # Get customer profile if exists
            if user['role'] == 'customer':
                customer = self.customer_model.get_customer_by_user_id(user['id'])
                if customer:
                    st.session_state.customer_id = customer['id']
            
            return True
        return False
    
    def register(self, username, email, password, role='customer'):
        """Register new user"""
        user_id = self.user_model.create_user(username, email, password, role)
        
        if user_id:
            # Create customer profile for customer role
            if role == 'customer':
                self.customer_model.create_customer(
                    first_name=username,
                    last_name='',
                    phone='',
                    email=email,
                    user_id=user_id
                )
            return True
        return False
    
    def logout(self):
        """Logout user"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.logged_in = False
    
    def is_admin(self):
        """Check if current user is admin"""
        return st.session_state.get('role') == 'admin'
    
    def is_staff(self):
        """Check if current user is staff or admin"""
        return st.session_state.get('role') in ['admin', 'staff']
    
    def is_customer(self):
        """Check if current user is customer"""
        return st.session_state.get('role') == 'customer'
