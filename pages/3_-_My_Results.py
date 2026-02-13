import streamlit as st
from datetime import datetime
import re

# Helper function to parse dates in multiple formats
def parse_date(date_string):
    """Parse date string with support for multiple formats"""
    formats = ["%m/%d/%y", "%Y-%m-%d", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    # If all formats fail, return a default date
    return datetime(1970, 1, 1)


def format_comment_markdown(text):
    """Format AI feedback into clean markdown lists."""
    if not text:
        return ""

    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]
    items = []

    for line in raw_lines:
        if "•" in line:
            parts = [part.strip() for part in line.split("•") if part.strip()]
            items.extend(parts)
        else:
            items.append(line)

    cleaned = []
    for item in items:
        cleaned_item = re.sub(r"^(?:[-*]|\d+\.|\d+\)|Step\s*\d+:)\s*", "", item, flags=re.IGNORECASE)
        cleaned.append(cleaned_item)

    if len(cleaned) > 1:
        return "\n".join([f"- {item}" for item in cleaned if item])

    return cleaned[0] if cleaned else ""

# Function to load feedback from other pages
def load_feedback_from_sessions():
    """
    Load feedback from mock_interview and resume pages into interviews_data
    This ensures comments are synced from other pages
    """
    if 'interviews_data' not in st.session_state:
        return
    # Mock interview feedback
    if 'interview_feedback' in st.session_state:
        for interview_id, feedback_data in st.session_state.interview_feedback.items():
            # Find the interview in interviews_data
            existing = next((item for item in st.session_state.interviews_data 
                           if item['id'] == interview_id), None)
            if existing and feedback_data:
                # Update score and comments from feedback
                existing['score'] = feedback_data.get('overall_score', existing['score'])
    
    # Resume feedback
    if 'resume_feedback' in st.session_state:
        for resume_id, feedback_data in st.session_state.resume_feedback.items():
            # Find the resume in interviews_data
            existing = next((item for item in st.session_state.interviews_data 
                           if item['id'] == resume_id), None)
            if existing and feedback_data:
                # Update score and comments from feedback
                existing['score'] = feedback_data.get('overall_score', existing['score'])

st.set_page_config(page_title="My Results", page_icon="📝", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 2])

with col1:
    st.image("assets/logo.jpeg", width=150)

with col2:
    st.title("My Interviews")

st.markdown("---")

# Load any feedback from other pages
load_feedback_from_sessions()

# Initialize interviews_data as empty on first load
if 'interviews_data' not in st.session_state:
    st.session_state.interviews_data = []

# Helper function to get color based on score
def get_score_color(score, item_type):
    if score >= 80:
        return "#87CEEB"  # Blue for 80+
    elif score >= 60:
        return "#90EE90"  # Green for 60-79
    elif score >= 40:
        return "#FFE66D"  # Yellow for 40-59
    else:
        return "#FF6B6B"  # Red for below 40

# CSS for card styling
st.markdown("""
    <style>
    .review-card {
        border: 3px solid black;
        border-radius: 20px;
        padding: 20px;
        margin: 10px;
        background-color: white;
        height: 300px;
        display: flex;
        flex-direction: column;
        position: relative;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .review-card:hover {
        transform: scale(1.02);
    }
    .score-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        color: black;
    }
    .card-content {
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #D3D3D3;
        font-size: 48px;
        font-weight: bold;
    }
    .card-footer {
        background-color: #FFE66D;
        margin: -20px;
        margin-top: 10px;
        padding: 15px;
        border-radius: 0 0 17px 17px;
        text-align: center;
        border-top: 3px solid black;
    }
    .card-footer.interview {
        background-color: #87CEEB;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .card-date {
        font-size: 16px;
        font-weight: bold;
    }
    .filter-button {
        padding: 10px 20px;
        margin: 5px;
        border-radius: 5px;
        border: 2px solid black;
        background-color: white;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for selected item
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# Top controls row
control_col1, control_col2, control_col3 = st.columns([1, 4, 1])

with control_col1:
    st.markdown("### 🔧 FILTERS")
    filter_option = st.selectbox("Filter by", ["All", "Resumes", "Interviews", "90%+", "80-89%", "70-79%", "Below 70%"], label_visibility="collapsed")

with control_col2:
    search_query = st.text_input("🔍 Search", placeholder="Search interviews and resumes...", label_visibility="collapsed")

with control_col3:
    st.markdown("### ⇅ SORT")
    sort_option = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Score (High to Low)", "Score (Low to High)"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Filter data based on selection
filtered_data = st.session_state.interviews_data.copy()

if filter_option == "Resumes":
    filtered_data = [item for item in filtered_data if item.get("type") == "resume"]
elif filter_option == "Interviews":
    filtered_data = [item for item in filtered_data if item.get("type") == "interview"]
elif filter_option == "90%+":
    filtered_data = [item for item in filtered_data if item["score"] >= 90]
elif filter_option == "80-89%":
    filtered_data = [item for item in filtered_data if 80 <= item["score"] < 90]
elif filter_option == "70-79%":
    filtered_data = [item for item in filtered_data if 70 <= item["score"] < 80]
elif filter_option == "Below 70%":
    filtered_data = [item for item in filtered_data if item["score"] < 70]

# Search filter
if search_query:
    filtered_data = [
        item for item in filtered_data
        if search_query.lower() in item.get("title", "").lower()
    ]

# Sort data
if sort_option == "Date (Newest)":
    filtered_data.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)
elif sort_option == "Date (Oldest)":
    filtered_data.sort(key=lambda x: parse_date(x.get("date", "")))
elif sort_option == "Score (High to Low)":
    filtered_data.sort(key=lambda x: x["score"], reverse=True)
elif sort_option == "Score (Low to High)":
    filtered_data.sort(key=lambda x: x["score"])

# Display detail view if an item is selected
if st.session_state.selected_item is not None:
    item = st.session_state.selected_item
    
    # Header with back button and score
    header_col1, header_col2, header_col3 = st.columns([1, 6, 1])
    
    with header_col1:
        score_color = get_score_color(item["score"], item.get("type", "interview"))
        st.markdown(f"""
            <div style="background-color: {score_color}; padding: 15px 25px; border-radius: 15px; 
                        font-size: 32px; font-weight: bold; text-align: center; border: 2px solid black;">
                {item["score"]}%
            </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        st.markdown(f"# {item.get('title', 'Result')}")
        st.markdown(f"**{item.get('date', '')}**")
    
    with header_col3:
        st.markdown("### 💬")
    
    # Content area with two columns (Feedback on the left under Back to List)
    sidebar_col, content_col = st.columns([1, 2])

    with sidebar_col:
        if st.button("← Back to List"):
            st.session_state.selected_item = None
            st.rerun()

        st.markdown("### Feedback & Notes")
        
        # Display existing comments in a styled format
        if item["comments"]:
            for comment in item["comments"]:
                # Display comment title as a bullet point
                st.markdown(f"**• {comment['title']}**")
                formatted_text = format_comment_markdown(comment.get("text", ""))
                if formatted_text:
                    st.markdown(formatted_text)
        else:
            st.info("No feedback available yet.")
        
        st.markdown("---")
        
        # Add manual comment section (optional)
        with st.expander("➕ Add Manual Note"):
            with st.form("comment_form", clear_on_submit=True):
                comment_title = st.text_input("Note Title")
                comment_text = st.text_area("Note Details")
                submit_button = st.form_submit_button("Add Note")
                
                if submit_button and comment_title and comment_text:
                    if "comments" not in item:
                        item["comments"] = []
                    item["comments"].append({
                        "title": comment_title,
                        "text": comment_text
                    })
                    st.success("Note added!")
                    st.rerun()

    with content_col:
        # Display Questions and Answers if available (for interviews)
        if item.get('type') == 'interview' and item.get('questions_and_answers'):
            st.markdown("### 📝 Interview Questions & Answers")
            for idx, qa in enumerate(item['questions_and_answers'], 1):
                with st.expander(f"Q{idx}: {qa['question'][:50]}..."):
                    st.markdown(f"**Question:** {qa['question']}")
                    st.markdown("**Your Answer:**")
                    st.info(qa['answer'])
                    
                    # Display feedback and score if available
                    if 'feedback' in qa:
                        st.markdown("**Feedback:**")
                        st.success(qa['feedback'])
                    if 'score' in qa:
                        st.markdown(f"**Score:** {qa['score']}/100")
    
else:
    # Display grid of cards
    if len(filtered_data) == 0:
        st.info("No items found matching your criteria.")
    else:
        # Create rows of 4 cards each
        num_cols = 4
        for i in range(0, len(filtered_data), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(filtered_data):
                    item = filtered_data[i + j]
                    with cols[j]:
                        score_color = get_score_color(item["score"], item.get("type", "interview"))
                        footer_class = "interview" if item.get("type") == "interview" else ""
                        
                        # Create clickable card
                        card_html = f"""
                            <div class="review-card">
                                <div class="score-badge" style="background-color: {score_color};">
                                    {item['score']}%
                                </div>
                                <div class="card-content">
                                    RESULT
                                </div>
                                <div class="card-footer {footer_class}">
                                    <div class="card-title">{item.get('title', 'Result')}</div>
                                    <div class="card-date">{item.get('date', '')}</div>
                                </div>
                            </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Button to select this item (hidden, triggered by card area)
                        if st.button(f"View Details", key=f"view_btn_{item['id']}", use_container_width=True):
                            st.session_state.selected_item = item
                            st.rerun()

