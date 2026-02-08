import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Mock Interview", page_icon="📝", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 4])

with col1:
    # Placeholder logo - replace with your own image
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)

with col2:
    st.title("Mock Interview")

st.markdown("---")

# ========================================
# YOUR CODE STARTS HERE
# ========================================

# Initialize session state for storing interview feedback
if 'interview_feedback' not in st.session_state:
    st.session_state.interview_feedback = {}

# Function to save interview feedback
def save_interview_feedback(interview_id, feedback_data):
    """
    Save feedback for a completed mock interview
    
    Args:
        interview_id: Unique identifier for the interview
        feedback_data: Dictionary containing:
            - overall_score: int (0-100)
            - strengths: list of strings
            - areas_for_improvement: list of strings
            - detailed_feedback: list of dicts with 'question' and 'feedback'
            - timestamp: datetime object
    """
    st.session_state.interview_feedback[interview_id] = feedback_data
    
    # Also update the interviews_data in session state for my_interviews page
    if 'interviews_data' not in st.session_state:
        st.session_state.interviews_data = []
    
    # Find existing interview or create new entry
    existing = next((item for item in st.session_state.interviews_data if item['id'] == interview_id), None)
    
    if existing:
        # Update existing interview with feedback
        existing['score'] = feedback_data['overall_score']
        existing['comments'] = []
        
        # Add strengths as comments
        if feedback_data.get('strengths'):
            existing['comments'].append({
                'title': '✅ Strengths',
                'text': '\n'.join(f"• {s}" for s in feedback_data['strengths'])
            })
        
        # Add areas for improvement
        if feedback_data.get('areas_for_improvement'):
            existing['comments'].append({
                'title': '🎯 Areas for Improvement',
                'text': '\n'.join(f"• {a}" for a in feedback_data['areas_for_improvement'])
            })
        
        # Add detailed question feedback
        if feedback_data.get('detailed_feedback'):
            for item in feedback_data['detailed_feedback']:
                existing['comments'].append({
                    'title': f"❓ {item['question']}",
                    'text': item['feedback']
                })

# PLACEHOLDER: Your mock interview logic here
st.info("🎤 Mock Interview functionality placeholder")
st.write("This is where your interview questions and recording logic will go.")

# Example usage - Remove this and integrate with your actual interview code
with st.expander("📝 Example: Generate Mock Feedback"):
    st.write("This is a demonstration of how to save feedback after an interview.")
    
    if st.button("Simulate Interview Completion"):
        # Example feedback data structure
        example_feedback = {
            'overall_score': 85,
            'strengths': [
                "Clear and confident communication",
                "Good use of STAR method in responses",
                "Demonstrated relevant experience"
            ],
            'areas_for_improvement': [
                "Could provide more specific examples",
                "Work on reducing filler words",
                "Maintain better eye contact"
            ],
            'detailed_feedback': [
                {
                    'question': 'Tell me about yourself',
                    'feedback': 'Good structure, but could be more concise. Try to keep it under 2 minutes.'
                },
                {
                    'question': 'Why do you want to work here?',
                    'feedback': 'Excellent connection between your values and company mission.'
                }
            ],
            'timestamp': datetime.now()
        }
        
        # Save the feedback (use actual interview ID from your interviews_data)
        save_interview_feedback(2, example_feedback)  # Example: Home Depot Interview
        st.success("✅ Feedback saved! Check 'My Interviews' page to see the comments.")
        st.info("💡 Tip: Navigate to My Interviews → Home Depot Interview to see the feedback.")

# Add your actual mock interview content here

# ========================================
# YOUR CODE ENDS HERE
# ========================================