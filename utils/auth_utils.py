# utils/auth_utils.py
import streamlit as st
import requests
from typing import Dict, Optional

# Configuration
API_BASE_URL = "http://localhost:8000"  # Your FastAPI backend

def init_session_state():
    """Initialize session state for authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}

def login_user(username: str, password: str) -> Dict:
    """Login user with your FastAPI backend"""
    try:
        # Use form data format for OAuth2PasswordRequestForm
        response = requests.post(
            f"{API_BASE_URL}/auth/token",
            data={
                "username": username,
                "password": password
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            # Store token in session
            st.session_state.authenticated = True
            st.session_state.token = data["access_token"]
            st.session_state.user_info = {"username": username}
            
            return {"success": True, "message": "Login successful!"}
        else:
            return {"success": False, "message": "Invalid credentials"}
            
    except requests.ConnectionError:
        return {"success": False, "message": "Cannot connect to server"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def signup_user(user_data: Dict) -> Dict:
    """Create new user account"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/",
            json=user_data
        )
        
        if response.status_code == 201:
            return {"success": True, "message": "Account created! Please login."}
        else:
            return {"success": False, "message": "Signup failed"}
            
    except Exception as e:
        return {"success": False, "message": str(e)}

def logout_user():
    """Clear session to logout"""
    for key in ['authenticated', 'token', 'user_info']:
        if key in st.session_state:
            del st.session_state[key]

def is_authenticated() -> bool:
    """Check if user is logged in"""
    return st.session_state.get('authenticated', False)

def get_token() -> Optional[str]:
    """Get current JWT token"""
    return st.session_state.get('token')

def get_headers() -> Dict:
    """Get headers with JWT token for API calls"""
    token = get_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}








# # utils/auth_utils.py
# import streamlit as st
# import requests
# from typing import Dict, Optional

# # Configuration
# API_BASE_URL = "http://localhost:8000"  # Your FastAPI backend

# def init_session_state():
#     """Initialize session state for authentication"""
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
#     if 'token' not in st.session_state:
#         st.session_state.token = None
#     if 'user_info' not in st.session_state:
#         st.session_state.user_info = {}

# def login_user(username: str, password: str) -> Dict:
#     """Login user with your FastAPI backend"""
#     try:
#         # Use form data format for OAuth2PasswordRequestForm
#         response = requests.post(
#             f"{API_BASE_URL}/auth/token",
#             data={
#                 "username": username,
#                 "password": password
#             }
#         )
        
#         if response.status_code == 200:
#             data = response.json()
#             # Store token in session
#             st.session_state.authenticated = True
#             st.session_state.token = data["access_token"]
#             st.session_state.user_info = {"username": username}
            
#             return {"success": True, "message": "Login successful!"}
#         else:
#             return {"success": False, "message": "Invalid credentials"}
            
#     except requests.ConnectionError:
#         return {"success": False, "message": "Cannot connect to server"}
#     except Exception as e:
#         return {"success": False, "message": str(e)}

# def signup_user(user_data: Dict) -> Dict:
#     """Create new user account"""
#     try:
#         response = requests.post(
#             f"{API_BASE_URL}/auth/",
#             json=user_data
#         )
        
#         if response.status_code == 201:
#             return {"success": True, "message": "Account created! Please login."}
#         else:
#             return {"success": False, "message": "Signup failed"}
            
#     except Exception as e:
#         return {"success": False, "message": str(e)}

# def logout_user():
#     """Clear session to logout"""
#     for key in ['authenticated', 'token', 'user_info']:
#         if key in st.session_state:
#             del st.session_state[key]

# def is_authenticated() -> bool:
#     """Check if user is logged in"""
#     return st.session_state.get('authenticated', False)

# def get_token() -> Optional[str]:
#     """Get current JWT token"""
#     return st.session_state.get('token')

# def get_headers() -> Dict:
#     """Get headers with JWT token for API calls"""
#     token = get_token()
#     if token:
#         return {"Authorization": f"Bearer {token}"}
#     return {}