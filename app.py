import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Fuel My Future",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Automatically redirect to Dashboard
st.switch_page("pages/1_-_Dashboard.py")