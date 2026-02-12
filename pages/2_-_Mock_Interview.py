import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Mock Interview", page_icon="📝", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 4])

with col1:
    st.image("assets/logo.jpeg", width=150)
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

if 'interview_completed' not in st.session_state:
    st.session_state.interview_completed = False

if 'current_interview_id' not in st.session_state:
    st.session_state.current_interview_id = None

if 'interviews_data' not in st.session_state:
    st.session_state.interviews_data = []

if 'interview_company' not in st.session_state:
    st.session_state.interview_company = ''

if 'interview_position' not in st.session_state:
    st.session_state.interview_position = ''

# Function to calculate interview score
def calculate_interview_score(answers):
    """Calculate score based on answer completeness and length"""
    total_score = 0
    question_scores = []
    
    for answer in answers:
        if not answer or answer.strip() == '':
            score = 0
        else:
            # Score based on answer length (simple scoring logic)
            word_count = len(answer.split())
            if word_count >= 50:
                score = 100
            elif word_count >= 30:
                score = 80
            elif word_count >= 15:
                score = 60
            elif word_count >= 5:
                score = 40
            else:
                score = 20
        
        question_scores.append(score)
        total_score += score
    
    overall_score = total_score // len(answers) if answers else 0
    return overall_score, question_scores

# Function to save interview feedback
def save_interview_feedback(interview_id, feedback_data):
    st.session_state.interview_feedback[interview_id] = feedback_data
    
    # Create or update interview in interviews_data
    existing_index = next((i for i, item in enumerate(st.session_state.interviews_data) 
                          if item.get('id') == interview_id), None)
    
    interview_entry = {
        'id': interview_id,
        'title': f"{feedback_data.get('company', 'Mock Interview')} Interview",
        'type': 'interview',
        'date': feedback_data['timestamp'].strftime("%m/%d/%y"),
        'time': feedback_data['timestamp'].strftime("%I:%M %p"),
        'company': feedback_data.get('company', 'Mock Interview'),
        'position': feedback_data.get('position', 'Practice Session'),
        'score': feedback_data['overall_score'],
        'status': 'Completed',
        'content': f"Interview for {feedback_data.get('position', 'Practice Session')}",
        'questions_and_answers': feedback_data.get('questions_and_answers', []),
        'comments': []
    }
    
    # Add strengths as comments
    if feedback_data.get('strengths'):
        interview_entry['comments'].append({
            'title': '✅ Strengths',
            'text': '\n'.join(f"• {s}" for s in feedback_data['strengths'])
        })
    
    # Add areas for improvement
    if feedback_data.get('areas_for_improvement'):
        interview_entry['comments'].append({
            'title': '🎯 Areas for Improvement',
            'text': '\n'.join(f"• {a}" for a in feedback_data['areas_for_improvement'])
        })
    
    # Add consolidated detailed question feedback (without question titles)
    if feedback_data.get('detailed_feedback'):
        # Extract unique feedback messages
        feedback_messages = set()
        for item in feedback_data['detailed_feedback']:
            feedback_messages.add(item['feedback'])
        
        # Add as bullet points if there are unique messages
        if feedback_messages:
            interview_entry['comments'].append({
                'title': '💭 Detailed Feedback',
                'text': '\n'.join(f"• {msg}" for msg in sorted(feedback_messages))
            })
    
    if existing_index is not None:
        st.session_state.interviews_data[existing_index] = interview_entry
    else:
        # Clear sample data on first real interview
        if st.session_state.get('has_sample_data', False):
            st.session_state.interviews_data = [interview_entry]
            st.session_state.has_sample_data = False
        else:
            st.session_state.interviews_data.append(interview_entry)

# Function to reset interview
def reset_interview():
    st.session_state.current_question = 0
    st.session_state.answers = [''] * len(st.session_state.questions)
    st.session_state.is_recording = False
    st.session_state.timer_start = None
    st.session_state.interview_completed = False
    st.session_state.current_interview_id = int(time.time())  # New unique ID
    st.session_state.interview_company = ''
    st.session_state.interview_position = ''

# Check if this is a new interview
if st.session_state.current_interview_id is None:
    st.session_state.current_interview_id = int(time.time())

# Display Results Page if interview is completed
if st.session_state.interview_completed:
    st.success("🎉 Interview Completed!")
    
    # Get the latest feedback
    feedback = st.session_state.interview_feedback.get(st.session_state.current_interview_id, {})
    
    # Display Results
    st.markdown("## 📊 Your Interview Results")
    
    # Score display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Score", f"{feedback.get('overall_score', 0)}/100")
    
    with col2:
        answered = sum(1 for a in st.session_state.answers if a.strip())
        st.metric("Questions Answered", f"{answered}/{len(st.session_state.questions)}")
    
    with col3:
        avg_length = sum(len(a.split()) for a in st.session_state.answers) // len(st.session_state.answers)
        st.metric("Avg Answer Length", f"{avg_length} words")
    
    st.markdown("---")
    
    # Detailed Feedback
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### ✅ Strengths")
        for strength in feedback.get('strengths', []):
            st.success(f"• {strength}")
    
    with col_right:
        st.markdown("### 🎯 Areas for Improvement")
        for area in feedback.get('areas_for_improvement', []):
            st.warning(f"• {area}")
    
    st.markdown("---")
    
    # Question-by-question breakdown
    st.markdown("### 📝 Question Breakdown")
    
    for i, item in enumerate(feedback.get('detailed_feedback', [])):
        with st.expander(f"Question {i+1}: {item['question'][:60]}..."):
            st.write("**Your Answer:**")
            st.info(st.session_state.answers[i] if st.session_state.answers[i] else "No answer provided")
            st.write("**Score:**", item.get('score', 'N/A'))
            st.write("**Feedback:**")
            st.write(item['feedback'])
    
    st.markdown("---")
    
    # Action buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🔄 Start New Interview", use_container_width=True, type="primary"):
            reset_interview()
            st.rerun()
    
    with btn_col2:
        if st.button("📊 View All Results", use_container_width=True):
            st.switch_page("pages/3_-_My_Results.py")
    
    with btn_col3:
        if st.button("🏠 Go to Home", use_container_width=True):
            reset_interview()
            st.switch_page("app.py")

else:
    # Normal Interview Flow
    # Interview Setup Section
    st.markdown("### Interview Setup")
    setup_col1, setup_col2 = st.columns(2)
    
    with setup_col1:
        company_input = st.text_input(
            "🏢 Company Name", 
            value=st.session_state.interview_company,
            placeholder="e.g., Google, Amazon, etc.",
            key="company_input"
        )
        st.session_state.interview_company = company_input
    
    with setup_col2:
        position_input = st.text_input(
            "💼 Position", 
            value=st.session_state.interview_position,
            placeholder="e.g., Software Engineer, Manager, etc.",
            key="position_input"
        )
        st.session_state.interview_position = position_input
    
    st.markdown("---")
    
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
                # Calculate scores
                overall_score, question_scores = calculate_interview_score(st.session_state.answers)
                
                # Generate strengths and improvements
                strengths = []
                improvements = []
                
                answered_count = sum(1 for a in st.session_state.answers if a.strip())
                
                if answered_count == len(st.session_state.questions):
                    strengths.append("Completed all questions")
                else:
                    improvements.append(f"Answer all questions ({answered_count}/{len(st.session_state.questions)} answered)")
                
                avg_words = sum(len(a.split()) for a in st.session_state.answers if a.strip()) // max(answered_count, 1)
                
                if avg_words >= 50:
                    strengths.append("Comprehensive and detailed answers")
                elif avg_words >= 30:
                    strengths.append("Good answer length")
                else:
                    improvements.append("Provide more detailed answers (aim for 30+ words)")
                
                if confidence_score >= 70:
                    strengths.append("High confidence level")
                elif confidence_score < 50:
                    improvements.append("Work on building confidence")
                
                # Create detailed feedback for each question
                detailed_feedback = []
                for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
                    word_count = len(a.split()) if a else 0
                    
                    if word_count >= 50:
                        feedback = "Excellent detailed response! Good depth and structure."
                    elif word_count >= 30:
                        feedback = "Good answer. Consider adding more specific examples."
                    elif word_count >= 15:
                        feedback = "Basic answer provided. Expand with more details and examples."
                    elif word_count > 0:
                        feedback = "Answer too brief. Aim for at least 30 words with specific examples."
                    else:
                        feedback = "No answer provided. Make sure to answer all questions."
                    
                    detailed_feedback.append({
                        'question': q,
                        'feedback': feedback,
                        'score': question_scores[i]
                    })
                
                # Create questions and answers list with feedback
                questions_and_answers = []
                for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
                    questions_and_answers.append({
                        'question': q,
                        'answer': a if a else 'No answer provided',
                        'feedback': detailed_feedback[i]['feedback'],
                        'score': detailed_feedback[i]['score']
                    })
                
                # Create feedback data
                company_name = st.session_state.interview_company if st.session_state.interview_company else 'Mock Interview Practice'
                position_name = st.session_state.interview_position if st.session_state.interview_position else 'General Interview'
                
                feedback_data = {
                    'overall_score': overall_score,
                    'confidence_level': confidence_score,
                    'company': company_name,
                    'position': position_name,
                    'strengths': strengths,
                    'areas_for_improvement': improvements,
                    'detailed_feedback': detailed_feedback,
                    'questions_and_answers': questions_and_answers,
                    'timestamp': datetime.now(),
                    'overall_notes': overall_feedback
                }
                
                # Save the feedback
                save_interview_feedback(st.session_state.current_interview_id, feedback_data)
                
                # Mark interview as completed
                st.session_state.interview_completed = True
                st.rerun()

