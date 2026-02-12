import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Mock Interview", page_icon="📝", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 4])

with col1:
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)

with col2:
    st.title("Mock Interview")

st.markdown("---")

# Initialize session state
if 'interview_feedback' not in st.session_state:
    st.session_state.interview_feedback = {}

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'questions' not in st.session_state:
    st.session_state.questions = [
        "Tell me about yourself and your background",
        "What are your greatest strengths?",
        "Describe a challenging project you worked on"
    ]

if 'answers' not in st.session_state:
    st.session_state.answers = [''] * len(st.session_state.questions)

if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

# Function to save interview feedback
def save_interview_feedback(interview_id, feedback_data):
    st.session_state.interview_feedback[interview_id] = feedback_data
    
    if 'interviews_data' not in st.session_state:
        st.session_state.interviews_data = []
    
    existing = next((item for item in st.session_state.interviews_data if item['id'] == interview_id), None)
    
    if existing:
        existing['score'] = feedback_data['overall_score']
        existing['comments'] = []
        
        if feedback_data.get('strengths'):
            existing['comments'].append({
                'title': '✅ Strengths',
                'text': '\n'.join(f"• {s}" for s in feedback_data['strengths'])
            })
        
        if feedback_data.get('areas_for_improvement'):
            existing['comments'].append({
                'title': '🎯 Areas for Improvement',
                'text': '\n'.join(f"• {a}" for a in feedback_data['areas_for_improvement'])
            })
        
        if feedback_data.get('detailed_feedback'):
            for item in feedback_data['detailed_feedback']:
                existing['comments'].append({
                    'title': f"❓ {item['question']}",
                    'text': item['feedback']
                })

# Main Layout: Sidebar + Main Content
sidebar_col, main_col = st.columns([1, 3])

# ========================================
# LEFT SIDEBAR - Questions & Feedback
# ========================================
with sidebar_col:
    st.subheader("📋 Questions")
    
    # Display all questions with navigation
    for i, q in enumerate(st.session_state.questions):
        if st.button(f"Q{i+1}", key=f"nav_q{i}", use_container_width=True):
            st.session_state.current_question = i
        
        # Show checkmark if answered
        if st.session_state.answers[i]:
            st.caption(f"✅ Answered")
        else:
            st.caption(f"❌ Not answered")
    
    st.markdown("---")
    
    # Feedback section in sidebar
    st.subheader("💭 Feedback")
    feedback_text = st.text_area(
        "Notes/Comments",
        placeholder="Add your notes here...",
        height=200,
        key="sidebar_feedback"
    )

# ========================================
# MAIN CONTENT AREA
# ========================================
with main_col:
    # Top section with Q1, Q2, Q3 boxes
    st.subheader("Interview Questions")
    q_cols = st.columns(3)
    
    for i, col in enumerate(q_cols):
        with col:
            status = "✅" if st.session_state.answers[i] else "⭕"
            if st.button(f"{status} Q{i+1}", key=f"top_q{i}", use_container_width=True):
                st.session_state.current_question = i
    
    st.markdown("---")
    
    # Main content: Current Question + Recording Section
    content_left, content_right = st.columns([2, 1])
    
    # Left: Current Question
    with content_left:
        current_q = st.session_state.current_question
        
        st.markdown(f"### Question {current_q + 1} of {len(st.session_state.questions)}")
        st.info(st.session_state.questions[current_q])
        
        # Answer input
        answer = st.text_area(
            "Your Answer:",
            value=st.session_state.answers[current_q],
            height=200,
            key=f"answer_input_{current_q}"
        )
        
        # Save answer
        if st.button("💾 Save Answer", use_container_width=True):
            st.session_state.answers[current_q] = answer
            st.success("Answer saved!")
        
        # Navigation buttons
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if current_q > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with nav_col2:
            if current_q < len(st.session_state.questions) - 1:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.answers[current_q] = answer
                    st.session_state.current_question += 1
                    st.rerun()
    
    # Right: Recording/Timer Section
    with content_right:
        st.markdown("### 🎙️ Recording")
        
        # Timer display
        if st.session_state.timer_start:
            elapsed = int(time.time() - st.session_state.timer_start)
            minutes = elapsed // 60
            seconds = elapsed % 60
            st.markdown(f"## ⏱️ {minutes:02d}:{seconds:02d}")
        else:
            st.markdown("## ⏱️ 00:00")
        
        # Recording controls
        if not st.session_state.is_recording:
            if st.button("🔴 Start Recording", use_container_width=True):
                st.session_state.is_recording = True
                st.session_state.timer_start = time.time()
                st.rerun()
        else:
            if st.button("⏹️ Stop Recording", use_container_width=True):
                st.session_state.is_recording = False
                st.session_state.timer_start = None
                st.rerun()
        
        st.markdown("---")
        
        # Recording status
        if st.session_state.is_recording:
            st.success("🔴 Recording in progress...")
        else:
            st.info("⭕ Not recording")
    
    st.markdown("---")
    
    # Bottom: Submit Feedback Section
    st.markdown("### 📤 Submit Feedback")
    
    submit_col1, submit_col2, submit_col3 = st.columns([2, 1, 1])
    
    with submit_col1:
        overall_feedback = st.text_area(
            "Overall Feedback",
            placeholder="How did you do overall?",
            height=100
        )
    
    with submit_col2:
        confidence_score = st.slider(
            "Confidence Level",
            min_value=0,
            max_value=100,
            value=50
        )
    
    with submit_col3:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🚀 Submit Interview", use_container_width=True, type="primary"):
            # Create feedback data
            feedback_data = {
                'overall_score': confidence_score,
                'strengths': ["Completed all questions"],
                'areas_for_improvement': ["Continue practicing"],
                'detailed_feedback': [
                    {'question': q, 'feedback': a if a else "No answer provided"} 
                    for q, a in zip(st.session_state.questions, st.session_state.answers)
                ],
                'timestamp': datetime.now()
            }
            
            save_interview_feedback(2, feedback_data)
            st.success("✅ Interview submitted successfully!")
            st.balloons()
