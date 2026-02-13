import streamlit as st
from google import genai as genai
import os
import yaml

# --- 1. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Fuel My Future", page_icon="🚀")

# --- 2. AI SETUP ---
try:
    with open('config.yaml', 'r') as f:
        file = yaml.safe_load(f)

    API_KEY = file['API_KEY']

    # Determine SDK version
    try:
        _GENAI_SDK = "google-genai"
        from google import genai
    except ImportError:
        try:
            _GENAI_SDK = "google-generativeai"
            import google.generativeai as genai
        except ImportError:
            genai = None
            _GENAI_SDK = None

    if genai is None:
        st.error("Missing Google AI SDK. Install `google-genai` or `google-generativeai`.")
        target_model = None
    elif _GENAI_SDK == "google-genai":
        # New SDK
        client = genai.Client(api_key=API_KEY)
        target_model = 'gemini-3-flash-preview'
    else:
        # Old SDK
        genai.configure(api_key=API_KEY)
        target_model = 'gemini-3-flash-preview'

except Exception as e:
    st.error(f"Connection Error: {e}")
    target_model = None

# --- 3. SESSION STATE INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "review_sent" not in st.session_state:
    st.session_state.review_sent = False
if "it_sent" not in st.session_state:
    st.session_state.it_sent = False
if "pending_ai_query" not in st.session_state:
    st.session_state.pending_ai_query = None

# --- 4. CUSTOM CSS ---
st.markdown("""
    <style>
    :root {
        --primary-navy: #1E3A8A;
        --primary-sky: #38BDF8;
        --accent-green: #10B981;
        --accent-orange: #F59E0B;
    }

    [data-testid="stSidebar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container { 
        padding-top: 2rem !important; 
        max-width: 100% !important;
    }

    /* Main Title Styling */
    .main-title { 
        text-align: center; 
        font-size: 4.5rem !important; 
        font-weight: 900; 
        margin-top: -20px !important; 
        margin-bottom: 10px !important; 
        color: var(--primary-navy);
        background: linear-gradient(135deg, var(--primary-navy) 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .main-jingle { 
        text-align: center; 
        font-style: italic; 
        color: #64748B; 
        font-size: 1.8rem !important; 
        margin-top: 0px !important; 
        margin-bottom: 30px !important; 
    }

    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 3px solid var(--primary-sky);
    }

    /* Navigation Cards */
    .nav-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 2px solid var(--primary-sky);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        display: block;
    }

    .nav-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
        border-color: var(--primary-navy);
    }

    .nav-card-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }

    .nav-card-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin: 0;
    }

    /* Streamlit Page Links Styling */
    div[data-testid="stPageLink-Link"] { 
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 2px solid var(--primary-sky);
        border-radius: 16px; 
        padding: 25px 30px; 
        transition: all 0.3s ease; 
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stPageLink-Link"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
        border-color: var(--primary-navy);
    }

    div[data-testid="stPageLink-Link"] p { 
        font-size: 1.6rem !important; 
        font-weight: 700 !important; 
        color: var(--primary-navy) !important;
        margin: 0 !important;
    }

    div[data-testid="stPageLink-Link"] span { 
        font-size: 2.5rem !important;
        margin-right: 10px;
    }

    /* Chat Container */
    .chat-container {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 15px;
        height: 500px;
        overflow-y: auto;
        margin-bottom: 15px;
        border: 2px solid #E2E8F0;
        scroll-behavior: smooth;
    }

    /* Chat Messages */
    .stChatMessage {
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-navy) 0%, #2563EB 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 10px;
        font-weight: 600;
        color: var(--primary-navy);
        padding: 10px;
    }

    /* Success Messages */
    .success-box {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid var(--accent-green);
        font-weight: 600;
        text-align: center;
        margin: 10px 0;
    }

    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        color: #78350F;
        padding: 12px;
        border-radius: 10px;
        border: 2px solid var(--accent-orange);
        font-size: 0.9rem;
        margin: 10px 0;
    }

    /* Text Areas and Inputs */
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        padding: 10px;
    }

    .stTextArea textarea:focus, .stTextInput input:focus, .stSelectbox select:focus {
        border-color: var(--primary-sky);
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1);
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-sky);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-navy);
    }

    /* Status Badge */
    .status-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-green) 0%, #34D399 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 10px;
    }

    /* Caption Text */
    .stCaption {
        color: #64748B !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


# --- 5. HELPER FUNCTIONS ---
def get_ai_response(prompt_text):
    """Get AI response with proper error handling"""
    try:
        if _GENAI_SDK == "google-genai":
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt_text
            )
        else:  # google-generativeai
            model = genai.GenerativeModel("gemini-3-flash-preview")
            response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f'❌ Error: {str(e)}'


def process_ai_query():
    """Process pending AI query"""
    if st.session_state.pending_ai_query and target_model:
        try:
            with st.spinner('🤔 AI is thinking...'):
                answer = get_ai_response(st.session_state.pending_ai_query)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}"
            })
        st.session_state.pending_ai_query = None


# Process any pending query
process_ai_query()

# --- 6. DASHBOARD LAYOUT ---
left_col, center_col, right_col = st.columns([1.2, 3.2, 1.6], gap="large")

# LEFT PANEL: Support & Reviews
with left_col:
    st.markdown("<div class='section-header'>🌟 Community & Help</div>", unsafe_allow_html=True)

    # --- Review Section ---
    with st.expander("⭐ Rate Our App", expanded=True):
        if not st.session_state.review_sent:
            rating = st.feedback("stars")
            feedback_text = st.text_area("Your Feedback", key="rev_input", height=100,
                                         placeholder="Tell us what you think...")
            if st.button("📤 Send Review", use_container_width=True):
                st.session_state.review_sent = True
                st.rerun()
        else:
            st.markdown("<div class='success-box'>✅ Thank you! Review sent successfully!</div>",
                        unsafe_allow_html=True)
            if st.button("✍️ Write Another Review", use_container_width=True):
                st.session_state.review_sent = False
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- IT Support Section ---
    with st.expander("📧 Contact Support", expanded=True):
        if not st.session_state.it_sent:
            issue_type = st.selectbox("Issue Type",
                                      ["IT Bug", "Account Help", "Feature Request"],
                                      key="it_type")
            issue_desc = st.text_area("Describe the issue...", key="it_note", height=100,
                                      placeholder="Please provide details...")
            if st.button("📨 Send to IT", use_container_width=True):
                st.session_state.it_sent = True
                st.rerun()
        else:
            st.markdown("<div class='success-box'>✅ Support ticket created!</div>",
                        unsafe_allow_html=True)
            if st.button("📝 Send Another Note", use_container_width=True):
                st.session_state.it_sent = False
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Info box
    st.markdown("""
        <div class='info-box'>
            💡 <strong>Quick Tip:</strong><br>
            Use FutureBot AI to get instant help with your career questions!
        </div>
    """, unsafe_allow_html=True)

# CENTER PANEL
with center_col:
    # Logo
    logo_path = "10000071901.png"
    if os.path.exists(logo_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_path, use_container_width=True)

    # Title
    st.markdown('<h1 class="main-title">Fuel My Future</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-jingle">"Igniting Careers, Engineering Success."</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation Cards - Check if pages exist, otherwise create placeholder
    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        # Check if mock_interview.py exists
        if os.path.exists("pages/2_-_Mock_Interview.py"):
            st.page_link("pages/2_-_Mock_Interview.py", label="Mock Interview", icon="🎙️", use_container_width=True)

        # Check if Document_Hub.py exists
        if os.path.exists("pages/5_-_Document_Hub.py"):
            st.page_link("pages/5_-_Document_Hub.py", label="Document Hub", icon="📁", use_container_width=True)
        else:
            st.markdown("""
                <a href="#" class="nav-card" onclick="return false;">
                    <div class="nav-card-icon">📁</div>
                    <div class="nav-card-title">Document Hub</div>
                </a>
            """, unsafe_allow_html=True)

    with nav_col2:
        # Check if my_results.py exists
        if os.path.exists("pages/3_-_My_Results.py"):
            st.page_link("pages/3_-_My_Results.py", label="My Results", icon="📊", use_container_width=True)
        else:
            st.markdown("""
                <a href="#" class="nav-card" onclick="return false;">
                    <div class="nav-card-icon">📊</div>
                    <div class="nav-card-title">My Results</div>
                </a>
            """, unsafe_allow_html=True)

        # Check if resume.py exists
        if os.path.exists("pages/4_-_Resume.py"):
            st.page_link("pages/4_-_Resume.py", label="Resume Builder", icon="📄", use_container_width=True)
        else:
            st.markdown("""
                <a href="#" class="nav-card" onclick="return false;">
                    <div class="nav-card-icon">📄</div>
                    <div class="nav-card-title">Resume Builder</div>
                </a>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Stats or Info Section
    stat_col1, stat_col2, stat_col3 = st.columns(3)

    with stat_col1:
        st.markdown("""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%); 
                        border-radius: 12px; border: 2px solid #38BDF8;'>
                <div style='font-size: 2.5rem; margin-bottom: 5px;'>🎯</div>
                <div style='font-size: 1.2rem; font-weight: 700; color: #1E3A8A;'>Practice</div>
                <div style='font-size: 0.9rem; color: #64748B;'>Mock Interviews</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col2:
        st.markdown("""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); 
                        border-radius: 12px; border: 2px solid #10B981;'>
                <div style='font-size: 2.5rem; margin-bottom: 5px;'>📈</div>
                <div style='font-size: 1.2rem; font-weight: 700; color: #1E3A8A;'>Track</div>
                <div style='font-size: 0.9rem; color: #64748B;'>Your Progress</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col3:
        st.markdown("""
            <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                        border-radius: 12px; border: 2px solid #F59E0B;'>
                <div style='font-size: 2.5rem; margin-bottom: 5px;'>🚀</div>
                <div style='font-size: 1.2rem; font-weight: 700; color: #1E3A8A;'>Succeed</div>
                <div style='font-size: 0.9rem; color: #64748B;'>Land Your Job</div>
            </div>
        """, unsafe_allow_html=True)

# RIGHT PANEL: AI Assistant
with right_col:
    st.markdown("<div class='section-header'>🤖 FutureBot AI</div>", unsafe_allow_html=True)

    if target_model:
        st.markdown(f"<div class='info-box'>🟢 <strong>Status:</strong> Online<br><small>{target_model}</small></div>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>🔴 <strong>Status:</strong> Offline<br><small>AI unavailable</small></div>",
                    unsafe_allow_html=True)

    # Chat container
    chat_container = st.container(height=500, border=True)

    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.markdown("""
                <div style='text-align: center; padding: 40px; color: #64748B;'>
                    <div style='font-size: 3rem; margin-bottom: 15px;'>💬</div>
                    <div style='font-size: 1.1rem; font-weight: 600; margin-bottom: 10px;'>Welcome to FutureBot!</div>
                    <div style='font-size: 0.9rem;'>Ask me anything about your career, resume, or interview prep.</div>
                </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything...", key="ai_chat_input"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.pending_ai_query = prompt
        st.rerun()

    # Quick action buttons
    st.markdown("### 🎯 Quick Actions")

    quick_col1, quick_col2 = st.columns(2)

    with quick_col1:
        if st.button("💼 Career Tips", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Give me 3 career tips for success"
            })
            st.session_state.pending_ai_query = "Give me 3 career tips for success"
            st.rerun()

    with quick_col2:
        if st.button("📝 Resume Help", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "How can I improve my resume?"
            })
            st.session_state.pending_ai_query = "How can I improve my resume?"
            st.rerun()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()