import streamlit as st
from datetime import datetime

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Fuel My Future | Document Hub",
    page_icon="📂",
    layout="wide"
)

# --------------------------------------------------
# 2. SESSION STATE INIT
# --------------------------------------------------
if "all_docs" not in st.session_state:
    st.session_state.all_docs = [
        {"id": 1, "title": "Tech Internship 2025", "date": "2025-06-12", "type": "Resume",
         "tldr": "Focuses on Java projects and hackathon wins."},
        {"id": 2, "title": "Robotics Club Lead Resume", "date": "2025-08-20", "type": "Resume",
         "tldr": "Highlights leadership and hardware troubleshooting."},
        {"id": 3, "title": "Summer Camp Counselor", "date": "2025-05-01", "type": "Resume",
         "tldr": "Emphasizes soft skills and communication."},
        {"id": 4, "title": "LinkedIn Headline Refresh", "date": "2025-01-15", "type": "LinkedIn Profile",
         "tldr": "Updated for 10th grade transition."},
        {"id": 5, "title": "Networking Summary v2", "date": "2025-03-10", "type": "LinkedIn Profile",
         "tldr": "Professional branding for tech mentors."},
        {"id": 6, "title": "Personal Brand Bio", "date": "2025-11-05", "type": "LinkedIn Profile",
         "tldr": "Focuses on future goals in AI Engineering."},
        {"id": 7, "title": "Google STEP Description", "date": "2025-03-20", "type": "Job Description",
         "tldr": "Detailed breakdown of freshman internship requirements."},
        {"id": 8, "title": "Meta Front-End Role", "date": "2025-04-15", "type": "Job Description",
         "tldr": "Breakdown of UI/UX design expectations."},
        {"id": 9, "title": "SpaceX Engineer Specs", "date": "2025-09-12", "type": "Job Description",
         "tldr": "Research on aerospace software standards."},
        {"id": 10, "title": "Youth Leadership Bio", "date": "2025-02-10", "type": "Professional Bio",
         "tldr": "Highlights community service roles."},
        {"id": 11, "title": "Speaker Intro - STEM", "date": "2025-10-30", "type": "Professional Bio",
         "tldr": "Short intro for public speaking."},
        {"id": 12, "title": "Hackathon Team Bio", "date": "2026-01-12", "type": "Professional Bio",
         "tldr": "Concise bio for project submissions."},
        {"id": 13, "title": "NHS Application Essay", "date": "2025-08-05", "type": "Other",
         "tldr": "Writing sample for Honor Society."},
        {"id": 14, "title": "Scholarship Cover Letter", "date": "2025-12-15", "type": "Other",
         "tldr": "Draft for STEM excellence grant."},
        {"id": 15, "title": "Volunteer Work Log", "date": "2026-01-20", "type": "Other",
         "tldr": "Tracking of hours and project impact."}
    ]

for d in st.session_state.all_docs:
    st.session_state.setdefault(f"rename_{d['id']}", False)
    st.session_state.setdefault(f"summary_{d['id']}", False)

# --------------------------------------------------
# 3. STYLING
# --------------------------------------------------
st.markdown("""
<style>
:root {
    --navy: #1E3A8A;
    --navy-accent: #1D4ED8;
    --sky: #38BDF8;
    --bg-light: #F8FAFC;
    --bg-dark: #0F172A;
    --text-light: #0F172A;
    --text-dark: #F8FAFC;
}

.stApp { background: var(--bg-light); color: var(--text-light); }
[data-theme="dark"] .stApp { background: var(--bg-dark); color: var(--text-dark); }

.main-header { font-size: 3.5rem; font-weight: 800; color: var(--navy); }
.navy-tagline { color: var(--navy-accent); margin-bottom: 40px; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 16px;
    border: 1px solid var(--navy);
}
[data-theme="dark"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #1E293B;
    border: 1px solid var(--sky);
}

.doc-title { line-height: 1.2; margin-bottom: 6px; }

[data-theme="dark"] .stButton>button {
    background:#1D4ED8; color:#F8FAFC; border:none;
}
[data-theme="dark"] input {
    background:#0F172A; color:#F8FAFC; border:1px solid #38BDF8;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 4. HEADER
# --------------------------------------------------
st.markdown("<h1 class='main-header'>Document Hub</h1>", unsafe_allow_html=True)
st.markdown("<p class='navy-tagline'>View your progress to becoming the future self you want to be!</p>",
            unsafe_allow_html=True)

# --------------------------------------------------
# 5. FILTERS
# --------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    sort_option = st.selectbox(
        "Sort By",
        ["Most to Least Recent", "Least to Most Recent", "Alphabetical (A-Z)"],
        key="sort_select"
    )
with c2:
    type_filter = st.selectbox(
        "Document Type",
        ["All Documents", "Resume", "LinkedIn Profile", "Job Description", "Professional Bio", "Other"],
        key="type_select"
    )

docs = st.session_state.all_docs
if type_filter != "All Documents":
    docs = [d for d in docs if d["type"] == type_filter]

if sort_option == "Alphabetical (A-Z)":
    docs = sorted(docs, key=lambda x: x["title"])
elif sort_option == "Most to Least Recent":
    docs = sorted(docs, key=lambda x: x["date"], reverse=True)
else:
    docs = sorted(docs, key=lambda x: x["date"])

# --------------------------------------------------
# 6. DOCUMENT GRID
# --------------------------------------------------
category_map = {
    "Resume": {"icon": "📄", "color": "#DBEAFE", "text": "#1E40AF"},
    "LinkedIn Profile": {"icon": "🌐", "color": "#F3E8FF", "text": "#6B21A8"},
    "Job Description": {"icon": "💼", "color": "#FFEDD5", "text": "#9A3412"},
    "Professional Bio": {"icon": "👤", "color": "#D1FAE5", "text": "#065F46"},
    "Other": {"icon": "📁", "color": "#F1F5F9", "text": "#475569"}
}

rows = [docs[i:i + 3] for i in range(0, len(docs), 3)]

for row in rows:
    cols = st.columns(3)
    for i, doc in enumerate(row):
        with cols[i]:
            with st.container(border=True):

                t1, t2 = st.columns([5, 1])
                with t1:
                    st.markdown(
                        f"<h3 class='doc-title'>{doc['title']}</h3>",
                        unsafe_allow_html=True
                    )

                with t2:
                    st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
                    with st.popover("⋮"):
                        if st.button("📝 Rename", key=f"rename_btn_{doc['id']}"):
                            st.session_state[f"rename_{doc['id']}"] ^= True
                        if st.button("✨ Summary", key=f"summary_btn_{doc['id']}"):
                            st.session_state[f"summary_{doc['id']}"] ^= True
                        if st.button("🗑️ Remove", key=f"delete_btn_{doc['id']}"):
                            st.session_state.all_docs = [
                                d for d in st.session_state.all_docs
                                if d["id"] != doc["id"]
                            ]
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                date_obj = datetime.strptime(doc["date"], "%Y-%m-%d")
                cat = category_map[doc["type"]]

                st.markdown(f"""
                <div style='margin-bottom:12px;'>
                    <span style='color:#64748B;font-size:0.85rem;'>
                        🗓 {date_obj.strftime('%m-%d-%Y')}
                    </span>
                    <span style='background:{cat["color"]};color:{cat["text"]};
                        padding:4px 12px;border-radius:20px;
                        font-size:0.8rem;font-weight:bold;margin-left:10px;'>
                        {cat["icon"]} {doc["type"]}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state[f"rename_{doc['id']}"]:
                    new_name = st.text_input(
                        "New name",
                        value=doc["title"],
                        key=f"rename_input_{doc['id']}"
                    )
                    if st.button("Save", key=f"save_{doc['id']}"):
                        doc["title"] = new_name
                        st.session_state[f"rename_{doc['id']}"] = False
                        st.rerun()

                if st.session_state[f"summary_{doc['id']}"]:
                    st.info(f"**AI Insight:** {doc['tldr']}")

# --------------------------------------------------
# 7. AI GROWTH SUITE
# --------------------------------------------------
st.markdown(
    "<h2 style='color: var(--navy); font-weight:900;'>🚀 AI Growth Suite</h2>",
    unsafe_allow_html=True
)

with st.expander("Analyze Professional Trajectory", expanded=True):

    tab1, tab2, tab3 = st.tabs(
        ["📊 Evolution Summary", "🔍 Growth Comparison", "💬 Personal AI Coach"]
    )

    with tab1:
        st.write("Generate a high-level summary of how your professional writing has evolved.")
        if st.button("Generate Portfolio Summary", key="gen_summary"):
            st.markdown("""
            **AI Executive Summary:**

            Your writing shows a clear evolution from **activity-based descriptions**
            to **impact-driven narratives**.

            - Increased use of measurable outcomes  
            - Stronger, action-oriented verbs  
            - Improved formatting for recruiter skimmability  

            Overall trajectory indicates growing professional maturity and clarity.
            """)

    with tab2:
        st.write("Compare two documents to identify writing improvements.")
        col_a, col_b = st.columns(2)

        with col_a:
            old_doc = st.selectbox(
                "Older Document",
                [d["title"] for d in st.session_state.all_docs],
                key="compare_old"
            )
        with col_b:
            new_doc = st.selectbox(
                "Newer Document",
                [d["title"] for d in st.session_state.all_docs],
                key="compare_new"
            )

        if st.button("Compare Improvements", key="compare_btn"):
            st.success(f"Comparison Complete: {old_doc} → {new_doc}")
            st.markdown("""
            **AI Growth Analysis:**
            1. **Verb Strength:** More decisive and leadership-focused verbs.
            2. **Conciseness:** Reduced redundancy and tighter bullet points.
            3. **Structure:** Improved visual hierarchy and white space usage.
            """)

    with tab3:
        with st.form("ai_coach_form"):
            question = st.text_input(
                "Ask the AI Coach about your writing growth:",
                key="coach_q"
            )
            submitted = st.form_submit_button("Ask Coach")

        if submitted:
            if question:
                st.info("""
                **AI is processing your response...**
                """)
            else:
                st.error("Please enter a question.")
