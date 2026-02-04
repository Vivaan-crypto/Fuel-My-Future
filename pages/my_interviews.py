import streamlit as st

st.set_page_config(page_title="My Interviews", page_icon="📝", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)
    # Placeholder logo - replace with your own image

with col2:
    st.title("My Interviews")

st.markdown("---")

# ========================================
# YOUR CODE STARTS HERE
# ========================================

# Add your content here


# ========================================
# YOUR CODE ENDS HERE
# ========================================