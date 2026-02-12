import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 4])

with col1:
    # Placeholder logo - replace with your own image
    st.image("assets/logo.jpeg", width=150)
with col2:
    st.title("Dashboard")

st.markdown("---")

# ========================================
# YOUR CODE STARTS HERE
# ========================================

# Add your content here

# ========================================
# YOUR CODE ENDS HERE
# ========================================
