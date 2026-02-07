import streamlit as st
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="Fuel My Future | Document Hub", page_icon="📂", layout="wide")

# 2. SESSION STATE INITIALIZATION
if 'all_docs' not in st.session_state:
    st.session_state.all_docs = [
        {"title": "Tech Internship 2025", "date": "2025-06-12", "type": "Resume",
         "tldr": "Focuses on Java projects and hackathon wins."},
        {"title": "Robotics Club Lead Resume", "date": "2025-08-20", "type": "Resume",
         "tldr": "Highlights leadership and hardware troubleshooting."},
        {"title": "Summer Camp Counselor", "date": "2025-05-01", "type": "Resume",
         "tldr": "Emphasizes soft skills and communication."},
        {"title": "LinkedIn Headline Refresh", "date": "2025-01-15", "type": "LinkedIn Profile",
         "tldr": "Updated for 10th grade transition."},
        {"title": "Networking Summary v2", "date": "2025-03-10", "type": "LinkedIn Profile",
         "tldr": "Professional branding for tech mentors."},
        {"title": "Personal Brand Bio", "date": "2025-11-05", "type": "LinkedIn Profile",
         "tldr": "Focuses on future goals in AI Engineering."},
        {"title": "Google STEP Description", "date": "2025-03-20", "type": "Job Description",
         "tldr": "Detailed breakdown of freshman internship requirements."},
        {"title": "Meta Front-End Role", "date": "2025-04-15", "type": "Job Description",
         "tldr": "Breakdown of UI/UX design expectations."},
        {"title": "SpaceX Engineer Specs", "date": "2025-09-12", "type": "Job Description",
         "tldr": "Research on aerospace software standards."},
        {"title": "Youth Leadership Bio", "date": "2025-02-10", "type": "Professional Bio",
         "tldr": "Highlights community service roles."},
        {"title": "Speaker Intro - STEM", "date": "2025-10-30", "type": "Professional Bio",
         "tldr": "Short intro for public speaking."},
        {"title": "Hackathon Team Bio", "date": "2026-01-12", "type": "Professional Bio",
         "tldr": "Concise bio for project submissions."},
        {"title": "NHS Application Essay", "date": "2025-08-05", "type": "Other",
         "tldr": "Writing sample for Honor Society."},
        {"title": "Scholarship Cover Letter", "date": "2025-12-15", "type": "Other",
         "tldr": "Draft for STEM excellence grant."},
        {"title": "Volunteer Work Log", "date": "2026-01-20", "type": "Other",
         "tldr": "Tracking of hours and project impact."}
    ]

# 3. STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background-color: #F8FAFC; }
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #0F172A; 
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }
    .navy-tagline {
        color: #1E3A8A; 
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }
    h3 { color: #1E3A8A !important; font-weight: 700 !important; }
    .stExpander { border: 2px solid #1E3A8A !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER SECTION
st.markdown('<h1 class="main-header">Document Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="navy-tagline">View your progress to becoming the future self you want to be!</p>',
            unsafe_allow_html=True)

# 5. FILTERS
col_f1, col_f2 = st.columns(2)
with col_f1:
    sort_option = st.selectbox("Sort By", ["Most to Least Recent", "Least to Most Recent", "Alphabetical (A-Z)"])
with col_f2:
    type_filter = st.selectbox("Document Type",
                               ["All Documents", "Resume", "LinkedIn Profile", "Job Description", "Professional Bio",
                                "Other"])

# 6. LOGIC
if type_filter == "All Documents":
    filtered = st.session_state.all_docs
else:
    filtered = [d for d in st.session_state.all_docs if d["type"] == type_filter]

if sort_option == "Alphabetical (A-Z)":
    filtered = sorted(filtered, key=lambda x: x["title"])
elif sort_option == "Most to Least Recent":
    filtered = sorted(filtered, key=lambda x: x["date"], reverse=True)
else:
    filtered = sorted(filtered, key=lambda x: x["date"])

st.write("##")

# 7. GRID DISPLAY
category_map = {
    "Resume": {"icon": "📄", "color": "#DBEAFE", "text": "#1E40AF"},
    "LinkedIn Profile": {"icon": "🌐", "color": "#F3E8FF", "text": "#6B21A8"},
    "Job Description": {"icon": "💼", "color": "#FFEDD5", "text": "#9A3412"},
    "Professional Bio": {"icon": "👤", "color": "#D1FAE5", "text": "#065F46"},
    "Other": {"icon": "📁", "color": "#F1F5F9", "text": "#475569"}
}

rows = [filtered[i:i + 3] for i in range(0, len(filtered), 3)]

for row_idx, row in enumerate(rows):
    cols = st.columns(3)
    for i, doc in enumerate(row):
        cat = category_map.get(doc['type'], category_map["Other"])
        with cols[i]:
            sum_key = f"s_{doc['title']}_{i}"
            ren_key = f"r_{doc['title']}_{i}"
            if sum_key not in st.session_state: st.session_state[sum_key] = False
            if ren_key not in st.session_state: st.session_state[ren_key] = False

            with st.container(border=True):
                # FIXED: Added '2' to st.columns
                t1, t2 = st.columns(2)
                with t1:
                    st.markdown(f"### {doc['title']}")
                with t2:
                    with st.popover("⋮"):
                        if st.button("📝 Rename", key=f"r_{i}_{doc['title']}", use_container_width=True):
                            st.session_state[ren_key] = not st.session_state[ren_key];
                            st.rerun()
                        if st.button("✨ Summary", key=f"s_{i}_{doc['title']}", use_container_width=True):
                            st.session_state[sum_key] = not st.session_state[sum_key];
                            st.rerun()
                        if st.button("🗑️ Remove", key=f"d_{i}_{doc['title']}", use_container_width=True):
                            st.session_state.all_docs.remove(doc);
                            st.rerun()

                date_obj = datetime.strptime(doc['date'], "%Y-%m-%d")
                st.markdown(f"""
                    <div style='margin-bottom: 15px;'>
                        <span style='color:#64748B; font-size:0.85rem;'>🗓 {date_obj.strftime("%m-%d-%Y")}</span>
                        <span style='background-color:{cat['color']}; color:{cat['text']}; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; margin-left: 10px;'>
                            {cat['icon']} {doc['type']}
                        </span>
                    </div>
                """, unsafe_allow_html=True)

                if st.session_state[ren_key]:
                    new_n = st.text_input("New Name:", value=doc['title'], key=f"in_{i}_{doc['title']}")
                    if st.button("Confirm", key=f"sv_{i}_{doc['title']}"):
                        doc['title'] = new_n;
                        st.session_state[ren_key] = False;
                        st.rerun()

                if st.session_state[sum_key]:
                    st.info(f"**AI Insight:** {doc['tldr']}")
                st.write("")

# 8. AI GROWTH SUITE
st.write("##")
st.markdown("<h2 style='color: #0F172A; font-weight: 900;'>🚀 AI Growth Suite</h2>", unsafe_allow_html=True)
with st.expander("Analyze Professional Trajectory", expanded=True):
    t1, t2, t3 = st.tabs(["📊 Evolution Summary", "🔍 Growth Comparison", "💬 Personal AI Coach"])

    with t1:
        st.write("Generate a comprehensive summary of your writing evolution.")
        if st.button("Generate Portfolio Summary", type="primary"):
            st.markdown("""
            **AI Executive Summary:**
            Your professional writing has evolved from a *descriptive* style to a *results-oriented* framework. 
            Since January 2025, you have increased your use of quantitative metrics by **40%**, 
            demonstrating a clearer understanding of your professional impact.
            """)

    with t2:
        st.write("Select two documents to see specific improvements in your professional voice.")
        # FIXED: Added '2' to st.columns
        ca, cb = st.columns(2)
        with ca: d1 = st.selectbox("Old Document", [d['title'] for d in st.session_state.all_docs], key="c1")
        with cb: d2 = st.selectbox("New Document", [d['title'] for d in st.session_state.all_docs], key="c2")

        if st.button("Compare Improvements"):
            st.success(f"Comparison Complete: '{d1}' vs '{d2}'")
            st.markdown(f"""
            **AI Growth Analysis:**
            1. **Verb Strength:** '{d2}' uses high-impact active verbs (*Spearheaded, Architected*) vs passive phrases in the older version.
            2. **Conciseness:** Word count decreased by 15%, increasing 'skimmability' for recruitment AI.
            3. **Formatting:** '{d2}' shows a 25% improvement in 'White Space' management and bullet point alignment.
            """)

    with t3:
        with st.form("ai_form", clear_on_submit=False):
            q = st.text_input("Ask about your writing growth:")
            if st.form_submit_button("Submit Question"):
                if q:
                    st.warning("**AI is processing your response...**")
                else:
                    st.error("Please enter a question.")
