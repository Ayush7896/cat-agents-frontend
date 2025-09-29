# views/about_me.py
import streamlit as st
import sys
import os
# Add parent directory to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth_utils import (
    init_session_state, 
    login_user, 
    signup_user, 
    is_authenticated, 
    logout_user
)

# Initialize session
init_session_state()

if not is_authenticated():
    # NOT LOGGED IN - Show login/signup
    st.title("Welcome to VARCly! 📚")
    st.write("Your personal CAT VARC mentor")
    
    # Create tabs for Login and Signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        
        # Simple login form
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            if username and password:
                with st.spinner("Logging in..."):
                    result = login_user(username, password)
                
                if result["success"]:
                    st.success(result["message"])
                    st.rerun()  # Refresh the page
                else:
                    st.error(result["message"])
            else:
                st.error("Please enter username and password")
    
    with tab2:
        st.subheader("Create Account")
        
        # Simple signup form
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        
        new_username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        phone = st.text_input("Phone (optional)")
        
        if st.button("Sign Up", type="primary"):
            # Basic validation
            if not all([first_name, last_name, new_username, email, new_password]):
                st.error("Please fill all required fields")
            elif new_password != confirm_password:
                st.error("Passwords don't match")
            else:
                # Create user data
                user_data = {
                    "username": new_username,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": new_password,
                    "role": "user",  # Default role
                    "phone_number": phone or ""
                }
                
                with st.spinner("Creating account..."):
                    result = signup_user(user_data)
                
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])

else:
    # LOGGED IN - Show your content
    col1, col2 = st.columns([10, 2])
    with col2:
        if st.button("Logout"):
            logout_user()
            st.rerun()
    
    # Your existing about me content
    st.title("Hi, I'm VARCly — your personal CAT VARC mentor")
    
    col1, col2 = st.columns(2, gap="small")
    with col2:
        st.write("Senior Data Analyst, assisting enterprises by supporting data-driven decision-making.")
    
    st.write("""
    I help you sharpen your Verbal Ability and Reading Comprehension skills through smart practice, 
    instant feedback, and interactive learning. Whether it's parajumbles, RCs, or vocab, 
    I make VARC prep simple, structured, and effective — so you can focus on acing the CAT with confidence.
    """)









# # views/about_me.py
# import streamlit as st
# import sys
# import os
# # Add parent directory to import utils
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from utils.auth_utils import (
#     init_session_state, 
#     login_user, 
#     signup_user, 
#     is_authenticated, 
#     logout_user
# )

# # Initialize session
# init_session_state()

# if not is_authenticated():
#     # NOT LOGGED IN - Show login/signup
#     st.title("Welcome to VARCly! 📚")
#     st.write("Your personal CAT VARC mentor")
    
#     # Create tabs for Login and Signup
#     tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
#     with tab1:
#         st.subheader("Login")
        
#         # Simple login form
#         username = st.text_input("Username", key="login_username")
#         password = st.text_input("Password", type="password", key="login_password")
        
#         if st.button("Login", type="primary"):
#             if username and password:
#                 with st.spinner("Logging in..."):
#                     result = login_user(username, password)
                
#                 if result["success"]:
#                     st.success(result["message"])
#                     st.rerun()  # Refresh the page
#                 else:
#                     st.error(result["message"])
#             else:
#                 st.error("Please enter username and password")
    
#     with tab2:
#         st.subheader("Create Account")
        
#         # Simple signup form
#         col1, col2 = st.columns(2)
#         with col1:
#             first_name = st.text_input("First Name")
#         with col2:
#             last_name = st.text_input("Last Name")
        
#         new_username = st.text_input("Username", key="signup_username")
#         email = st.text_input("Email")
#         new_password = st.text_input("Password", type="password", key="signup_password")
#         confirm_password = st.text_input("Confirm Password", type="password")
#         phone = st.text_input("Phone (optional)")
        
#         if st.button("Sign Up", type="primary"):
#             # Basic validation
#             if not all([first_name, last_name, new_username, email, new_password]):
#                 st.error("Please fill all required fields")
#             elif new_password != confirm_password:
#                 st.error("Passwords don't match")
#             else:
#                 # Create user data
#                 user_data = {
#                     "username": new_username,
#                     "email": email,
#                     "first_name": first_name,
#                     "last_name": last_name,
#                     "password": new_password,
#                     "role": "user",  # Default role
#                     "phone_number": phone or ""
#                 }
                
#                 with st.spinner("Creating account..."):
#                     result = signup_user(user_data)
                
#                 if result["success"]:
#                     st.success(result["message"])
#                 else:
#                     st.error(result["message"])

# else:
#     # LOGGED IN - Show your content
#     col1, col2 = st.columns([10, 2])
#     with col2:
#         if st.button("Logout"):
#             logout_user()
#             st.rerun()
    
#     # Your existing about me content
#     st.title("Hi, I'm VARCly — your personal CAT VARC mentor")
    
#     col1, col2 = st.columns(2, gap="small")
#     with col2:
#         st.write("Senior Data Analyst, assisting enterprises by supporting data-driven decision-making.")
    
#     st.write("""
#     I help you sharpen your Verbal Ability and Reading Comprehension skills through smart practice, 
#     instant feedback, and interactive learning. Whether it's parajumbles, RCs, or vocab, 
#     I make VARC prep simple, structured, and effective — so you can focus on acing the CAT with confidence.
#     """)