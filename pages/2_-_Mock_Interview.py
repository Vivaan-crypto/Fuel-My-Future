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

if 'interview_completed' not in st.session_state:
    st.session_state.interview_completed = False

if 'current_interview_id' not in st.session_state:
    st.session_state.current_interview_id = None

if 'interviews_data' not in st.session_state:
    st.session_state.interviews_data = []

# Function to analyze answer quality
def analyze_answer_quality(answer, question):
    """Analyze answer quality based on multiple factors"""
    if not answer or answer.strip() == '':
        return {
            'score': 0,
            'word_count': 0,
            'sentence_count': 0,
            'has_examples': False,
            'relevance': 'none'
        }
    
    # Basic metrics
    words = answer.split()
    word_count = len(words)
    sentences = answer.split('.')
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Check for examples/specifics (STAR method indicators)
    example_keywords = ['example', 'instance', 'time when', 'situation', 'project', 
                        'experience', 'specifically', 'resulted in', 'achieved', 'led to']
    has_examples = any(keyword in answer.lower() for keyword in example_keywords)
    
    # Check for repetitive words (gibberish detection)
    unique_words = len(set(word.lower() for word in words))
    word_diversity = unique_words / word_count if word_count > 0 else 0
    
    # Check for very short repeated words (like "a a a a a")
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    # Question relevance check (basic)
    question_keywords = question.lower().split()
    relevance_score = sum(1 for word in words if word.lower() in question_keywords)
    
    # Calculate base score
    score = 0
    
    # Length scoring (0-40 points)
    if word_count >= 50:
        score += 40
    elif word_count >= 30:
        score += 30
    elif word_count >= 15:
        score += 20
    elif word_count >= 5:
        score += 10
    
    # Sentence structure (0-20 points)
    if sentence_count >= 3:
        score += 20
    elif sentence_count >= 2:
        score += 10
    elif sentence_count >= 1:
        score += 5
    
    # Examples/specificity (0-20 points)
    if has_examples:
        score += 20
    
    # Word diversity bonus (0-20 points) - penalize gibberish
    if word_diversity > 0.7:
        score += 20
    elif word_diversity > 0.5:
        score += 10
    elif word_diversity > 0.3:
        score += 5
    else:
        score = max(0, score - 30)  # Heavy penalty for low diversity (gibberish)
    
    # Average word length check (gibberish typically has very short words)
    if avg_word_length < 2:
        score = max(0, score - 20)
    
    # Cap at 100
    score = min(100, score)
    
    return {
        'score': score,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'has_examples': has_examples,
        'word_diversity': word_diversity,
        'avg_word_length': avg_word_length
    }

# Function to generate detailed feedback
def generate_detailed_feedback(answer, question, analysis):
    """Generate specific, actionable feedback"""
    feedback_parts = []
    
    score = analysis.get('score', 0)
    word_count = analysis.get('word_count', 0)
    has_examples = analysis.get('has_examples', False)
    word_diversity = analysis.get('word_diversity', 0)
    
    # Overall quality assessment
    if score >= 80:
        feedback_parts.append("Strong response overall.")
    elif score >= 60:
        feedback_parts.append("Good foundation, but could be enhanced.")
    elif score >= 40:
        feedback_parts.append("Basic answer provided, needs more development.")
    else:
        feedback_parts.append("Needs significant improvement.")
    
    # Specific critiques and suggestions
    if word_count == 0:
        feedback_parts.append("No answer provided. Make sure to respond to every question.")
    elif word_count < 20:
        feedback_parts.append(f"Answer is too brief ({word_count} words). Aim for at least 30-50 words to adequately address the question.")
    elif word_count < 30:
        feedback_parts.append("Consider expanding your answer with more details and context.")
    
    # Check for gibberish/low quality
    if word_diversity < 0.4 and word_count > 10:
        feedback_parts.append("⚠️ Your answer appears to contain repetitive or nonsensical content. Focus on providing meaningful, diverse responses.")
    
    if analysis.get('avg_word_length', 0) < 2.5 and word_count > 10:
        feedback_parts.append("⚠️ Answer quality concern detected. Ensure you're using complete, professional language.")
    
    # Examples and specificity
    if not has_examples and score > 0:
        if "yourself" in question.lower():
            feedback_parts.append("Include specific details about your background, skills, and relevant experiences.")
        elif "strengths" in question.lower():
            feedback_parts.append("Provide concrete examples that demonstrate each strength you mention.")
        elif "project" in question.lower() or "challenge" in question.lower():
            feedback_parts.append("Use the STAR method (Situation, Task, Action, Result) to structure your response with specific examples.")
        else:
            feedback_parts.append("Add specific examples or instances to support your points.")
    
    # Structure suggestions
    if analysis.get('sentence_count', 0) < 2 and word_count > 15:
        feedback_parts.append("Break your response into multiple sentences for better clarity and flow.")
    
    # Positive reinforcement
    if has_examples:
        feedback_parts.append("✓ Good use of specific examples.")
    
    if word_diversity > 0.7:
        feedback_parts.append("✓ Diverse vocabulary and well-articulated points.")
    
    if analysis.get('sentence_count', 0) >= 3:
        feedback_parts.append("✓ Well-structured response with multiple points.")
    
    return " ".join(feedback_parts)

# Function to calculate interview score
def calculate_interview_score(answers, questions):
    """Calculate score based on answer quality analysis"""
    total_score = 0
    question_scores = []
    all_analyses = []
    
    for answer, question in zip(answers, questions):
        analysis = analyze_answer_quality(answer, question)
        question_scores.append(analysis['score'])
        all_analyses.append(analysis)
        total_score += analysis['score']
    
    overall_score = total_score // len(answers) if answers else 0
    return overall_score, question_scores, all_analyses

# Function to save interview feedback
def save_interview_feedback(interview_id, feedback_data):
    st.session_state.interview_feedback[interview_id] = feedback_data
    
    # Create or update interview in interviews_data
    existing_index = next((i for i, item in enumerate(st.session_state.interviews_data) 
                          if item.get('id') == interview_id), None)
    
    interview_entry = {
        'id': interview_id,
        'date': feedback_data['timestamp'].strftime("%Y-%m-%d"),
        'time': feedback_data['timestamp'].strftime("%I:%M %p"),
        'company': feedback_data.get('company', 'Mock Interview'),
        'position': feedback_data.get('position', 'Practice Session'),
        'score': feedback_data['overall_score'],
        'status': 'Completed',
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
    
    # Add detailed question feedback
    if feedback_data.get('detailed_feedback'):
        for item in feedback_data['detailed_feedback']:
            interview_entry['comments'].append({
                'title': f"❓ {item['question'][:50]}...",
                'text': item['feedback']
            })
    
    if existing_index is not None:
        st.session_state.interviews_data[existing_index] = interview_entry
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

# Check if this is a new interview
if st.session_state.current_interview_id is None:
    st.session_state.current_interview_id = int(time.time())

# Display Results Page if interview is completed
if st.session_state.interview_completed:
    st.balloons()
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
        total_words = sum(len(a.split()) for a in st.session_state.answers if a.strip())
        avg_length = total_words // max(answered, 1)
        st.metric("Avg Answer Length", f"{avg_length} words")
    
    st.markdown("---")
    
    # Detailed Feedback
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### ✅ Strengths")
        if feedback.get('strengths'):
            for strength in feedback.get('strengths', []):
                st.success(f"• {strength}")
        else:
            st.info("Keep practicing to develop your strengths!")
    
    with col_right:
        st.markdown("### 🎯 Areas for Improvement")
        if feedback.get('areas_for_improvement'):
            for area in feedback.get('areas_for_improvement', []):
                st.warning(f"• {area}")
        else:
            st.info("Great job! Keep up the good work.")
    
    st.markdown("---")
    
    # Question-by-question breakdown
    st.markdown("### 📝 Question Breakdown")
    
    for i, item in enumerate(feedback.get('detailed_feedback', [])):
        with st.expander(f"Question {i+1} - Score: {item.get('score', 0)}/100 - {item['question'][:60]}..."):
            st.write("**Your Answer:**")
            st.info(st.session_state.answers[i] if st.session_state.answers[i] else "No answer provided")
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
        
        # Right: Timer Section
        with content_right:
            st.markdown("### ⏱️ Timer")
            
            # Timer display
            if st.session_state.timer_start:
                elapsed = int(time.time() - st.session_state.timer_start)
                minutes = elapsed // 60
                seconds = elapsed % 60
                st.markdown(f"## {minutes:02d}:{seconds:02d}")
            else:
                st.markdown("## 00:00")
            
            # Timer controls
            if not st.session_state.is_recording:
                if st.button("▶️ Start Timer", use_container_width=True):
                    st.session_state.is_recording = True
                    st.session_state.timer_start = time.time()
                    st.rerun()
            else:
                if st.button("⏸️ Stop Timer", use_container_width=True):
                    st.session_state.is_recording = False
                    st.session_state.timer_start = None
                    st.rerun()
            
            st.markdown("---")
            
            # Timer status
            if st.session_state.is_recording:
                st.success("⏱️ Timer running...")
            else:
                st.info("⏱️ Timer stopped")
        
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
                # Calculate scores with detailed analysis
                overall_score, question_scores, analyses = calculate_interview_score(
                    st.session_state.answers, 
                    st.session_state.questions
                )
                
                # Generate strengths and improvements based on analysis
                strengths = []
                improvements = []
                
                answered_count = sum(1 for a in st.session_state.answers if a.strip())
                
                if answered_count == len(st.session_state.questions):
                    strengths.append("Completed all questions")
                else:
                    improvements.append(f"Answer all questions ({answered_count}/{len(st.session_state.questions)} answered)")
                
                # Check average word diversity (quality indicator)
                if analyses and len(analyses) > 0:
                    avg_diversity = sum(a.get('word_diversity', 0) for a in analyses) / len(analyses)
                    if avg_diversity > 0.7:
                        strengths.append("High-quality, diverse vocabulary throughout responses")
                    elif avg_diversity < 0.4:
                        improvements.append("Focus on providing meaningful, varied responses (avoid repetition)")
                
                # Check for use of examples
                example_count = sum(1 for a in analyses if a.get('has_examples', False))
                if example_count >= 2:
                    strengths.append("Good use of specific examples and details")
                elif example_count == 0:
                    improvements.append("Include specific examples using the STAR method (Situation, Task, Action, Result)")
                
                # Overall score assessment
                if overall_score >= 80:
                    strengths.append("Strong overall interview performance")
                elif overall_score >= 60:
                    strengths.append("Solid foundation with room for improvement")
                elif overall_score < 40:
                    improvements.append("Focus on providing complete, thoughtful answers to each question")
                
                # Confidence correlation
                if confidence_score >= 70:
                    strengths.append("High self-confidence")
                elif confidence_score < 50:
                    improvements.append("Build confidence through more practice and preparation")
                
                # Create detailed feedback for each question
                detailed_feedback = []
                for i, (q, a, analysis) in enumerate(zip(st.session_state.questions, st.session_state.answers, analyses)):
                    feedback = generate_detailed_feedback(a, q, analysis)
                    
                    detailed_feedback.append({
                        'question': q,
                        'feedback': feedback,
                        'score': question_scores[i]
                    })
                
                # Create feedback data
                feedback_data = {
                    'overall_score': overall_score,
                    'confidence_level': confidence_score,
                    'company': 'Mock Interview Practice',
                    'position': 'General Interview',
                    'strengths': strengths if strengths else ["Keep practicing!"],
                    'areas_for_improvement': improvements if improvements else ["Continue refining your responses"],
                    'detailed_feedback': detailed_feedback,
                    'timestamp': datetime.now(),
                    'overall_notes': overall_feedback
                }
                
                # Save the feedback
                save_interview_feedback(st.session_state.current_interview_id, feedback_data)
                
                # Mark interview as completed
                st.session_state.interview_completed = True
                st.rerun()