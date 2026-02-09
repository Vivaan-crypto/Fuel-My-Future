import streamlit as st
from datetime import datetime
from pdf2image import convert_from_bytes
import io

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# ========================================
# CUSTOM CSS
# ========================================
st.markdown("""
<style>
    :root {
        --primary-navy: #1E3A8A;
        --primary-sky: #38BDF8;
        --accent-green: #10B981;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary-navy);
        margin-bottom: 0.5rem;
    }

    .sub-header {
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .chat-messages {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 15px;
        height: 600px;
        overflow-y: auto;
        margin-bottom: 15px;
    }

    .user-message {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px 20%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .ai-message {
        background: linear-gradient(135deg, #38BDF8 0%, #7DD3FC 100%);
        color: #0F172A;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 20% 8px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .system-message {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        color: white;
        padding: 10px 14px;
        border-radius: 12px;
        margin: 8px auto;
        text-align: center;
        max-width: 80%;
        font-size: 0.9rem;
    }

    .upload-area {
        border: 3px dashed var(--primary-sky);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        margin: 20px 0;
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--primary-navy) 0%, #2563EB 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-sky);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SESSION STATE
# ========================================
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'uploaded_resume' not in st.session_state:
    st.session_state.uploaded_resume = None
if 'pdf_images' not in st.session_state:
    st.session_state.pdf_images = []


# ========================================
# HELPER FUNCTIONS
# ========================================
def convert_pdf_to_images(pdf_file):
    """Convert PDF to images using pdf2image"""
    try:
        pdf_bytes = pdf_file.read()
        images = convert_from_bytes(pdf_bytes, dpi=200)
        return images
    except Exception as e:
        st.error(f"Error loading PDF: {str(e)}")
        return []


def save_to_my_uploads(resume_file):
    """Save resume to My Uploads"""
    if 'all_docs' not in st.session_state:
        st.session_state.all_docs = []

    new_id = max([doc['id'] for doc in st.session_state.all_docs], default=0) + 1

    new_doc = {
        'id': new_id,
        'title': resume_file.name.replace('.pdf', ''),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': 'Resume',
        'tldr': f"AI analyzed resume - uploaded {datetime.now().strftime('%m/%d/%Y')}"
    }

    st.session_state.all_docs.append(new_doc)
    return True


# ========================================
# HEADER
# ========================================
col1, col2 = st.columns([1, 4])

with col1:
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)

with col2:
    st.markdown("<h1 class='main-header'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Upload your resume and chat with AI for feedback</p>", unsafe_allow_html=True)

st.markdown("---")

# ========================================
# UPLOAD INTERFACE
# ========================================
if st.session_state.uploaded_resume is None:
    st.markdown("""
        <div class='upload-area'>
            <h2 style='color: #1E3A8A; margin-bottom: 20px;'>🚀 Ready to Optimize Your Resume?</h2>
            <p style='color: #64748B; font-size: 1.1rem;'>Upload your resume (PDF format) to get started</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose your resume PDF",
        type=['pdf'],
        help="Upload a PDF version of your resume"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_resume = uploaded_file
        with st.spinner("Loading PDF..."):
            st.session_state.pdf_images = convert_pdf_to_images(uploaded_file)
        st.session_state.chat_messages.append({
            'type': 'system',
            'content': f'📁 Resume uploaded: {uploaded_file.name}'
        })
        st.rerun()

# ========================================
# ANALYSIS INTERFACE
# ========================================
else:
    # Action buttons
    button_col1, button_col2, button_col3 = st.columns([2, 2, 2])

    with button_col1:
        if st.button("💾 Save to My Uploads", use_container_width=True):
            if save_to_my_uploads(st.session_state.uploaded_resume):
                st.success("✅ Resume saved to My Uploads!")
                st.session_state.chat_messages.append({
                    'type': 'system',
                    'content': '💾 Resume saved successfully'
                })

    with button_col2:
        if st.button("🔄 Upload New Resume", use_container_width=True):
            st.session_state.uploaded_resume = None
            st.session_state.chat_messages = []
            st.session_state.pdf_images = []
            st.rerun()

    with button_col3:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

    st.markdown("---")

    # Main layout
    pdf_col, chat_col = st.columns([1, 1])

    # PDF VIEWER
    with pdf_col:
        st.markdown("### 📄 Resume Preview")

        if st.session_state.pdf_images:
            for i, img in enumerate(st.session_state.pdf_images):
                st.image(img, use_container_width=True, caption=f"Page {i + 1}")
        else:
            st.info("Loading PDF preview...")

    # CHAT INTERFACE
    with chat_col:
        st.markdown("### 💬 AI Assistant")

        # Display messages
        chat_container = st.container()

        with chat_container:
            st.markdown("<div class='chat-messages'>", unsafe_allow_html=True)

            for message in st.session_state.chat_messages:
                if message['type'] == 'user':
                    st.markdown(f"<div class='user-message'>👤 {message['content']}</div>", unsafe_allow_html=True)
                elif message['type'] == 'ai':
                    st.markdown(f"<div class='ai-message'>🤖 {message['content']}</div>", unsafe_allow_html=True)
                elif message['type'] == 'system':
                    st.markdown(f"<div class='system-message'>{message['content']}</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Chat input
        with st.form(key='chat_form', clear_on_submit=True):
            col1, col2 = st.columns([5, 1])

            with col1:
                user_input = st.text_input(
                    "Ask about your resume...",
                    placeholder="e.g., How can I improve my resume?",
                    label_visibility="collapsed"
                )

            with col2:
                submit_button = st.form_submit_button("Send")

            if submit_button and user_input:
                # Add user message
                st.session_state.chat_messages.append({
                    'type': 'user',
                    'content': user_input
                })

                # PLACEHOLDER: Gemini AI will replace this
                st.session_state.chat_messages.append({
                    'type': 'ai',
                    'content': '🤖 AI is working on your request...'
                })

                st.rerun()

        # Quick questions
        st.markdown("### 🎯 Quick Questions")

        quick_col1, quick_col2 = st.columns(2)

        with quick_col1:
            if st.button("💪 Strengths", use_container_width=True):
                st.session_state.chat_messages.append({'type': 'user', 'content': 'What are my strengths?'})
                st.session_state.chat_messages.append({'type': 'ai', 'content': '🤖 AI is working on your request...'})
                st.rerun()

            if st.button("📈 Improvements", use_container_width=True):
                st.session_state.chat_messages.append({'type': 'user', 'content': 'How can I improve?'})
                st.session_state.chat_messages.append({'type': 'ai', 'content': '🤖 AI is working on your request...'})
                st.rerun()

        with quick_col2:
            if st.button("🎯 ATS Tips", use_container_width=True):
                st.session_state.chat_messages.append({'type': 'user', 'content': 'ATS optimization tips?'})
                st.session_state.chat_messages.append({'type': 'ai', 'content': '🤖 AI is working on your request...'})
                st.rerun()

            if st.button("📊 Score", use_container_width=True):
                st.session_state.chat_messages.append({'type': 'user', 'content': 'What is my score?'})
                st.session_state.chat_messages.append({'type': 'ai', 'content': '🤖 AI is working on your request...'})
                st.rerun()