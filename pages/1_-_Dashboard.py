import streamlit as st
import google.generativeai as genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Fuel My Future", page_icon="🚀")

# --- 2. AI SETUP ---
try:
    genai.configure(api_key="AIzaSyDu-67jy3ONlflRt6T0Wtn9VBwa6soUYFo")
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = 'gemini-3-flash-preview'
    if f"models/{target_model}" not in available_models and available_models:
        target_model = available_models[0].replace('models/', '')
    model = genai.GenerativeModel(target_model)
except Exception as e:
    st.error(f"Connection Error: {e}")

# --- 3. SESSION STATE INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "review_sent" not in st.session_state:
    st.session_state.review_sent = False
if "it_sent" not in st.session_state:
    st.session_state.it_sent = False

# --- 4. CUSTOM CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    .block-container { padding-top: 2rem !important; }

    /* Side Column Positioning */
    [data-testid="column"]:first-child, [data-testid="column"]:last-child {
        position: relative;
        top: 120px;
    }

    h2, .stSubheader {
        padding-top: 20px !important;
        font-size: 1.6rem !important;
        white-space: nowrap !important;
        color: #1E1E1E;
    }

    .main-title { text-align: center; font-size: 4.8rem !important; font-weight: 900; margin-top: -30px !important; margin-bottom: 0px !important; color: #1E1E1E; }
    .main-jingle { text-align: center; font-style: italic; color: #555; font-size: 2rem !important; margin-top: 5px !important; margin-bottom: 40px !important; }
    
    div[data-testid="stPageLink-Link"] { 
        background-color: #fcfcfc; 
        border-radius: 15px; 
        padding: 20px 30px; 
        transition: all 0.2s ease; 
        margin-bottom: 15px; 
        border: 2px solid #f0f2f6; 
    }
    div[data-testid="stPageLink-Link"] p { font-size: 2.5rem !important; font-weight: 800 !important; color: #1E1E1E !important; }
    div[data-testid="stPageLink-Link"] span { font-size: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD LAYOUT ---
left_col, center_col, right_col = st.columns([1.2, 3.2, 1.6], gap="medium")

# LEFT PANEL: Support & Reviews with Logic
with left_col:
    st.subheader("Community & Help")
    
    # --- Review Section ---
    with st.expander("⭐ Rate Our App", expanded=True):
        if not st.session_state.review_sent:
            st.feedback("stars")
            st.text_area("Your Feedback", key="rev_input", height=100)
            if st.button("Send Review", use_container_width=True):
                st.session_state.review_sent = True
                st.rerun()
        else:
            st.success("✅ Review Sent!")
            if st.button("Write Another Review"):
                st.session_state.review_sent = False
                st.rerun()

    st.divider()

    # --- IT Support Section ---
    with st.expander("📧 Contact Support", expanded=True):
        if not st.session_state.it_sent:
            st.selectbox("Issue Type", ["IT Bug", "Account Help", "Feature Request"], key="it_type")
            st.text_area("Describe the issue...", key="it_note", height=100)
            if st.button("Send to IT", use_container_width=True):
                st.session_state.it_sent = True
                st.rerun()
        else:
            st.success("✅ Note sent to IT!")
            if st.button("Send Another Note"):
                st.session_state.it_sent = False
                st.rerun()

# CENTER PANEL
with center_col:
    logo_path = "10000071901.png"
    _, logo_col, _ = st.columns([1, 3.5, 1])
    with logo_col:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
            
    st.markdown('<h1 class="main-title">Fuel My Future</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-jingle">"Igniting Careers, Engineering Success."</p>', unsafe_allow_html=True)

    st.page_link("pages/2_-_Mock_Interview.py", label="Mock Interview", icon="🎙️", use_container_width=True)
    st.page_link("pages/3_-_My_Results.py", label="My Results", icon="📅", use_container_width=True)
    st.page_link("pages/4_-_Resume.py", label="Resume Builder", icon="📄", use_container_width=True)
    st.page_link("pages/5_-_Document_Hub.py", label="Document Hub", icon="📁", use_container_width=True)

# RIGHT PANEL: AI Assistant
with right_col:
    st.subheader("🤖 FutureBot AI") 
    if 'target_model' in locals():
        st.caption(f"Status: Online ({target_model})")
        
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").markdown(prompt)
        
        try:
            response = model.generate_content(prompt)
            answer = response.text
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            with chat_container:
                st.chat_message("assistant").markdown(answer)
        except Exception as e:
            st.error(f"AI Error: {e}")
