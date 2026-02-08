import streamlit as st
from datetime import datetime

st.set_page_config(page_title="My Interviews", page_icon="📝", layout="wide")

# Top bar with logo and title
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)
    # Placeholder logo 

with col2:
    st.title("My Interviews")

st.markdown("---")

# Hardcoded data, can replace if needed
if 'interviews_data' not in st.session_state:
    st.session_state.interviews_data = [
        {
            "id": 1,
            "title": "Chick Fil A Resume",
            "type": "resume",
            "date": "02/01/26",
            "score": 92,
            "content": "Resume content here...",
            "comments": []
        },
        {
            "id": 2,
            "title": "Home Depot Interview",
            "type": "interview",
            "date": "01/28/26",
            "score": 78,
            "content": "Interview notes here...",
            "comments": []
        },
        {
            "id": 3,
            "title": "Chick Fil A Interview",
            "type": "interview",
            "date": "01/17/26",
            "score": 73,
            "content": "Interview notes here...",
            "comments": []
        },
        {
            "id": 4,
            "title": "Kroger Interview",
            "type": "interview",
            "date": "12/23/25",
            "score": 84,
            "content": "Interview notes here...",
            "comments": []
        },
    ]

# Helper function to get color based on score
def get_score_color(score, item_type):
    if item_type == "interview":
        return "#87CEEB"  # Light blue for interviews
    elif score >= 90:
        return "#90EE90"  # Light green
    elif score >= 80:
        return "#FFE66D"  # Light yellow
    elif score >= 70:
        return "#FFB347"  # Light orange
    else:
        return "#FF6B6B"  # Light red

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
    filtered_data = [item for item in filtered_data if item["type"] == "resume"]
elif filter_option == "Interviews":
    filtered_data = [item for item in filtered_data if item["type"] == "interview"]
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
    filtered_data = [item for item in filtered_data if search_query.lower() in item["title"].lower()]

# Sort data
if sort_option == "Date (Newest)":
    filtered_data.sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%y"), reverse=True)
elif sort_option == "Date (Oldest)":
    filtered_data.sort(key=lambda x: datetime.strptime(x["date"], "%m/%d/%y"))
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
        score_color = get_score_color(item["score"], item["type"])
        st.markdown(f"""
            <div style="background-color: {score_color}; padding: 15px 25px; border-radius: 15px; 
                        font-size: 32px; font-weight: bold; text-align: center; border: 2px solid black;">
                {item["score"]}%
            </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        st.markdown(f"# {item['title']}")
        st.markdown(f"**{item['date']}**")
    
    with header_col3:
        st.markdown("### 💬")
    
    if st.button("← Back to List"):
        st.session_state.selected_item = None
        st.rerun()
    
    st.markdown("---")
    
    # Content area with two columns
    content_col1, content_col2 = st.columns([2, 1])
    
    with content_col1:
        st.markdown("### Document Preview")
        st.info("📄 Document content would be displayed here. You can integrate a PDF viewer or display formatted content.")
        st.markdown(f"```\n{item['content']}\n```")
    
    with content_col2:
        st.markdown("### Comments")
        
        # Display existing comments
        if item["comments"]:
            for comment in item["comments"]:
                st.markdown(f"**• {comment['title']}**")
                st.markdown(f"{comment['text']}")
                st.markdown("---")
        else:
            st.info("No comments yet. Add your feedback below!")
        
        # Add new comment
        with st.form("comment_form", clear_on_submit=True):
            comment_title = st.text_input("Comment Title")
            comment_text = st.text_area("Comment Details")
            submit_button = st.form_submit_button("Add Comment")
            
            if submit_button and comment_title and comment_text:
                if "comments" not in item:
                    item["comments"] = []
                item["comments"].append({
                    "title": comment_title,
                    "text": comment_text
                })
                st.success("Comment added!")
                st.rerun()

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
                        score_color = get_score_color(item["score"], item["type"])
                        footer_class = "interview" if item["type"] == "interview" else ""
                        
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
                                    <div class="card-title">{item['title']}</div>
                                    <div class="card-date">{item['date']}</div>
                                </div>
                            </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Button to select this item (hidden, triggered by card area)
                        if st.button(f"View Details###{item['id']}", key=f"btn_{item['id']}", use_container_width=True):
                            st.session_state.selected_item = item
                            st.rerun()

