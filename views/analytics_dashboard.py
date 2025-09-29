import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth_utils import is_authenticated, get_headers

# Check if logged in
if not is_authenticated():
    st.error("Please login to access analytics")
    st.stop()

st.title("Analytics Dashboard 📊")

# Simple metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Questions Attempted", "0")
with col2:
    st.metric("Accuracy", "0%")
with col3:
    st.metric("Streak", "0 days")

st.info("Analytics will be populated from your backend API")

# Example of how to call your backend
# headers = get_headers()
# response = requests.get(
#     "http://localhost:8000/analytics/user-stats",
#     headers=headers
# )