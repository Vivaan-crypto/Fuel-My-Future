import streamlit as st
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="Document Hub", page_icon="📂", layout="wide")

# 2. SESSION STATE INITIALIZATION
if 'all_docs' not in st.session_state:
    st.session_state.all_docs = []
if 'other_docs' not in st.session_state:
    st.session_state.other_docs = []

# 3. STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');

    /* FIX: Removed hardcoded background so Dark Mode works */

    .main-header {
        font-family: 'Inter', sans-serif;
        color: var(--text-color); /* FIX: Adapts to theme */
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }
    .navy-tagline {
        color: #3B82F6; /* FIX: Visible in both modes */
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--background-color); /* FIX: Adapts to theme */
        border: 1px solid rgba(128, 128, 128, 0.2); /* FIX: Visible in both modes */
        border-radius: 16px;
    }
    h3 { color: var(--text-color) !important; font-weight: 700 !important; }
    .stExpander { border: 1px solid #3B82F6 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER SECTION WITH LOGO
col1, col2 = st.columns([1, 4])

with col1:
    st.image("assets/logo.jpeg", width=150)
with col2:
    st.markdown('<h1 class="main-header">Document Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="navy-tagline">View your progress to becoming the future self you want to be!</p>',
                unsafe_allow_html=True)

st.markdown("---")

# 5. TABS
tab1, tab2 = st.tabs(["Resume History", "Other Documents"])

# ========================================
# HISTORY TAB
# ========================================
with tab1:
    # FILTERS
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sort_option = st.selectbox("Sort By", ["Most to Least Recent", "Least to Most Recent", "Alphabetical (A-Z)"])
    with col_f2:
        type_filter = st.selectbox("Document Type",
                                   ["All Documents"])

    # LOGIC
    if type_filter == "All Documents":
        filtered = [d for d in st.session_state.all_docs if d.get("type") == "Resume"]
    else:
        filtered = [d for d in st.session_state.all_docs if d.get("type") == type_filter]

    if sort_option == "Alphabetical (A-Z)":
        filtered = sorted(filtered, key=lambda x: x["title"])
    elif sort_option == "Most to Least Recent":
        filtered = sorted(filtered, key=lambda x: x["date"], reverse=True)
    else:
        filtered = sorted(filtered, key=lambda x: x["date"])

    st.write("##")

    # GRID DISPLAY
    # FIX: Category Map with high-contrast colors
    category_map = {
        "Resume": {"icon": "📄", "color": "#2563EB", "text": "white"},
        "LinkedIn Profile": {"icon": "🌐", "color": "#7C3AED", "text": "white"},
        "Job Description": {"icon": "💼", "color": "#EA580C", "text": "white"},
        "Professional Bio": {"icon": "👤", "color": "#059669", "text": "white"},
        "Other": {"icon": "📁", "color": "#475569", "text": "white"}
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
                    t1, t2 = st.columns([4, 1])
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
                    # FIX: color #94A3B8 is clear in Light and Dark mode
                    st.markdown(f"""
                        <div style='margin-bottom: 15px;'>
                            <span style='color: #94A3B8; font-size:0.9rem;'>🗓 {date_obj.strftime("%m-%d-%Y")}</span>
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

    # AI GROWTH SUITE (FUNCTIONALITY RETAINED)
    st.write("##")
    st.markdown(f"<h2 style='color: var(--text-color); font-weight: 900;'>🚀 AI Growth Suite</h2>", unsafe_allow_html=True)
    with st.expander("Analyze Professional Trajectory", expanded=True):
        t1, t2, t3 = st.tabs(["📊 Evolution Summary", "🔍 Growth Comparison", "💬 Personal AI Coach"])

        with t1:
            st.write("Generate a comprehensive summary of your writing evolution.")
            if st.button("Generate Portfolio Summary", type="primary"):
                st.markdown("""
                **AI Executive Summary:**
                Your professional writing has evolved from a *descriptive* style to a *results-oriented* framework. 
                You have increased your use of quantitative metrics by **40%**, 
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

# ========================================
# OTHER DOCUMENTS TAB
# ========================================
with tab2:
    st.write("##")
    
    # Upload section
    uploaded_file = st.file_uploader("Upload a document (PDF format)", type=['pdf'])
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Document name input
        doc_name = st.text_input("Document Name:", value=uploaded_file.name.replace('.pdf', ''))
        
        # Category dropdown (non-resume docs only)
        doc_category = st.selectbox(
            "Category:",
            ["Elevator Pitch", "LinkedIn Profile", "Job Description", "Professional Bio", "Other"]
        )
        
        # Date input
        doc_date = st.text_input("Date (YYYY-MM-DD):", value=datetime.now().strftime("%Y-%m-%d"))
        
        # Save button
        if st.button("💾 Save Document", type="primary"):
            # Validate date format
            try:
                datetime.strptime(doc_date, "%Y-%m-%d")
                
                # Create new other document entry
                new_doc = {
                    "title": doc_name,
                    "date": doc_date,
                    "type": doc_category,
                    "tldr": f"Uploaded on {datetime.now().strftime('%m/%d/%Y')}"
                }
                
                # Add to session state
                st.session_state.other_docs.append(new_doc)
                
                st.success("✅ Document saved successfully!")
                st.balloons()
                
            except ValueError:
                st.error("❌ Invalid date format. Please use YYYY-MM-DD")
    
    st.write("##")
    st.markdown("---")
    st.write("##")
    
    # Display uploaded documents in same layout as History tab
    st.markdown(f"<h2 style='color: var(--text-color); font-weight: 900;'> 📂 Your Uploaded Documents</h2>", unsafe_allow_html=True)
    
    st.write("##")
    
    # Use same category map
    category_map = {
        "Elevator Pitch": {"icon": "📄", "color": "#2563EB", "text": "white"},
        "LinkedIn Profile": {"icon": "🌐", "color": "#7C3AED", "text": "white"},
        "Job Description": {"icon": "💼", "color": "#EA580C", "text": "white"},
        "Professional Bio": {"icon": "👤", "color": "#059669", "text": "white"},
        "Other": {"icon": "📁", "color": "#475569", "text": "white"}
    }
    
    # Display all other documents in grid layout
    all_docs_sorted = sorted(st.session_state.other_docs, key=lambda x: x["date"], reverse=True)
    rows = [all_docs_sorted[i:i + 3] for i in range(0, len(all_docs_sorted), 3)]

    for row_idx, row in enumerate(rows):
        cols = st.columns(3)
        for i, doc in enumerate(row):
            cat = category_map.get(doc['type'], category_map["Other"])
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### {doc['title']}")
                    
                    date_obj = datetime.strptime(doc['date'], "%Y-%m-%d")
                    st.markdown(f"""
                        <div style='margin-bottom: 15px;'>
                            <span style='color: #94A3B8; font-size:0.9rem;'>🗓 {date_obj.strftime("%m-%d-%Y")}</span>
                            <span style='background-color:{cat['color']}; color:{cat['text']}; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; margin-left: 10px;'>
                                {cat['icon']} {doc['type']}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
