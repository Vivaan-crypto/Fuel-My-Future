import streamlit as st
from datetime import datetime
import base64
import yaml
import tempfile
import os
import time

try:
    from google import genai as genai

    _GENAI_SDK = "google-genai"
except ImportError:
    try:
        import google.generativeai as genai

        _GENAI_SDK = "google-generativeai"
    except ImportError:
        genai = None
        _GENAI_SDK = None

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

    .pdf-viewer {
        width: 100%;
        height: 800px;
        border: 2px solid var(--primary-navy);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

    .thinking-message {
        background: linear-gradient(135deg, #94A3B8 0%, #CBD5E1 100%);
        color: #0F172A;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 20% 8px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-style: italic;
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

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .thinking-dots {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# LOAD CONFIG AND SETUP CLIENT
# ========================================
with open('config.yaml', 'r') as f:
    file = yaml.safe_load(f)

API_KEY = file['API_KEY']
client = None

if genai is None:
    st.error("Missing Google AI SDK. Install `google-genai` or `google-generativeai`.")
elif hasattr(genai, "Client"):
    client = genai.Client(api_key=API_KEY)
else:
    genai.configure(api_key=API_KEY)
    client = genai.GenerativeModel("gemini-3-flash-preview")

# ========================================
# SESSION STATE
# ========================================
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'uploaded_resume' not in st.session_state:
    st.session_state.uploaded_resume = None
if 'pdf_base64' not in st.session_state:
    st.session_state.pdf_base64 = None
if 'uploaded_file_ref' not in st.session_state:
    st.session_state.uploaded_file_ref = None
if 'initial_review_done' not in st.session_state:
    st.session_state.initial_review_done = False
if 'processing' not in st.session_state:
    st.session_state.processing = False


# ========================================
# HELPER FUNCTIONS
# ========================================
def get_ai_response(prompt_text):
    """Get AI response with proper error handling"""
    try:
        if _GENAI_SDK == "google-genai":
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    st.session_state.uploaded_file_ref,
                    prompt_text
                ]
            )
        else:  # google-generativeai
            response = client.generate_content([
                st.session_state.uploaded_file_ref,
                prompt_text
            ])
        return response.text
    except Exception as e:
        return f'❌ Error: {str(e)}'


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
    st.image("assets/logo.jpeg", width=150)
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
        st.session_state.pdf_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
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
            st.session_state.pdf_base64 = None
            st.session_state.uploaded_file_ref = None
            st.session_state.initial_review_done = False
            st.rerun()

    with button_col3:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.initial_review_done = False
            st.rerun()

    st.markdown("---")

    # Main layout
    pdf_col, chat_col = st.columns([1, 1])

    # PDF VIEWER
    with pdf_col:
        st.markdown("### 📄 Resume Preview")

        if st.session_state.pdf_base64:
            # Upload the file to Gemini ONCE when first loaded
            if st.session_state.uploaded_file_ref is None:
                with st.spinner("Uploading PDF to Gemini AI..."):
                    try:
                        # Save base64 to temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(base64.b64decode(st.session_state.pdf_base64))
                            tmp_path = tmp_file.name

                        # Upload to Gemini based on SDK version
                        if _GENAI_SDK == "google-genai":
                            uploaded_file = client.files.upload(file=tmp_path)
                        else:  # google-generativeai
                            uploaded_file = genai.upload_file(path=tmp_path)

                        st.session_state.uploaded_file_ref = uploaded_file

                        # Clean up temp file
                        try:
                            os.unlink(tmp_path)
                        except:
                            pass

                        st.success("✅ PDF uploaded to Gemini AI")
                        st.session_state.chat_messages.append({
                            'type': 'system',
                            'content': '✅ PDF ready for AI analysis'
                        })

                        # Trigger initial review
                        st.rerun()

                    except Exception as e:
                        st.error(f"Upload error: {str(e)}")
                        st.session_state.chat_messages.append({
                            'type': 'system',
                            'content': f'❌ Upload failed: {str(e)}'
                        })

            # Display PDF
            pdf_display = f'<iframe src="data:application/pdf;base64,{st.session_state.pdf_base64}" class="pdf-viewer" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.info("No PDF to display")

    # CHAT INTERFACE
    with chat_col:
        st.markdown("### 💬 AI Assistant")

        # Display messages container
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

            # Show thinking indicator if processing
            if st.session_state.processing:
                st.markdown(
                    "<div class='thinking-message'><span class='thinking-dots'>🤔 AI is thinking...</span></div>",
                    unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Auto-generate initial review when PDF is uploaded
        if st.session_state.uploaded_file_ref and not st.session_state.initial_review_done:
            st.session_state.initial_review_done = True
            st.session_state.processing = True

            # Add system message
            st.session_state.chat_messages.append({
                'type': 'system',
                'content': '🔍 Generating initial resume analysis...'
            })
            st.rerun()

        # Process initial review
        if st.session_state.processing and st.session_state.initial_review_done and len(
                [m for m in st.session_state.chat_messages if m['type'] == 'ai']) == 0:
            initial_prompt = """Please provide a comprehensive review of this resume including:

1. Overall impression and score (1-10)
2. Key strengths
3. Areas for improvement
4. ATS optimization suggestions
5. Recommended next steps

Please be specific and actionable in your feedback."""

            ai_response = get_ai_response(initial_prompt)

            st.session_state.chat_messages.append({
                'type': 'ai',
                'content': ai_response
            })
            st.session_state.processing = False
            st.rerun()

        # Chat input
        user_input = st.text_input(
            "Ask about your resume...",
            placeholder="e.g., How can I improve my resume?",
            key="chat_input",
            label_visibility="collapsed"
        )

        if st.button("Send", use_container_width=True) and user_input:
            # Add user message immediately
            st.session_state.chat_messages.append({
                'type': 'user',
                'content': user_input
            })

            # Set processing flag
            st.session_state.processing = True
            st.rerun()

        # Process user query if we're in processing state
        if st.session_state.processing and st.session_state.chat_messages[-1]['type'] == 'user':
            last_user_message = st.session_state.chat_messages[-1]['content']

            if st.session_state.uploaded_file_ref:
                ai_response = get_ai_response(last_user_message)

                st.session_state.chat_messages.append({
                    'type': 'ai',
                    'content': ai_response
                })
            else:
                st.session_state.chat_messages.append({
                    'type': 'ai',
                    'content': '❌ Please wait for the PDF to finish uploading to Gemini AI.'
                })

            st.session_state.processing = False
            st.rerun()

        # Quick questions
        st.markdown("### 🎯 Quick Questions")

        quick_col1, quick_col2 = st.columns(2)

        with quick_col1:
            if st.button("💪 Strengths", use_container_width=True):
                st.session_state.chat_messages.append({
                    'type': 'user',
                    'content': 'What are the key strengths in my resume?'
                })
                st.session_state.processing = True
                st.rerun()

            if st.button("📈 Improvements", use_container_width=True):
                st.session_state.chat_messages.append({
                    'type': 'user',
                    'content': 'How can I improve my resume?'
                })
                st.session_state.processing = True
                st.rerun()

        with quick_col2:
            if st.button("🎯 ATS Tips", use_container_width=True):
                st.session_state.chat_messages.append({
                    'type': 'user',
                    'content': 'What are your ATS optimization tips?'
                })
                st.session_state.processing = True
                st.rerun()

            if st.button("📊 Score", use_container_width=True):
                st.session_state.chat_messages.append({
                    'type': 'user',
                    'content': 'What is my resume score?'
                })
                st.session_state.processing = True
                st.rerun()