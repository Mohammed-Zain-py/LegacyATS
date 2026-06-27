import streamlit as st
import requests

# 1. Page Config (Includes the fix to hide the developer menu)
st.set_page_config(
    page_title="LegacyATS Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# 2. Polished Theme Styling
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-size: 18px; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #161b22; text-align: center; padding: 12px; font-size: 14px; color: #8b949e; border-top: 1px solid #30363d; z-index: 100; }
    .score-banner { background-color: #1f242c; padding: 30px; border-radius: 8px; border-left: 6px solid #ff7b72; margin-bottom: 20px; }
    .pass-banner { border-left: 6px solid #238636; }
    .recruiter-welcome { background-color: #161b22; border: 1px solid #21262d; padding: 30px; border-radius: 8px; margin-bottom: 25px; }
    .keyword-tag { display: inline-block; background-color: #21262d; border: 1px solid #30363d; padding: 6px 12px; border-radius: 4px; margin: 4px; font-family: monospace; font-size: 16px; }
    .tag-found { color: #58a6ff; border-color: #388bfd; }
    .tag-missing { color: #f85149; border-color: #da3633; }
    .correction-terminal { background-color: #040406; border: 1px solid #30363d; padding: 20px; border-radius: 6px; font-family: 'Courier New', monospace; color: #79c0ff; white-space: pre-wrap; line-height: 1.6; font-size: 16px; }
    h1, h2, h3, h4 { color: #ffffff; }
    p { font-size: 18px; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
st.sidebar.title("System Control Panel")
st.sidebar.markdown("### API Key Authentication")
st.sidebar.markdown("""
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account.
3. Click **Get API Key**.
4. Create a key and paste it below.
""")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", placeholder="AIzaSy...")

st.sidebar.markdown("---")
st.sidebar.markdown("**System Limits:**")
st.sidebar.markdown("- 5 requests per minute limit.")
st.sidebar.markdown("- Max file size: 5MB.")

st.title("LegacyATS: ATS Resume Analyzer")

# 4. Tabs Routing (Recruiter Landing Page First)
tab1, tab2 = st.tabs(["Interactive Recruiter Workspace", "Live ATS Analysis Pipeline"])

# ---------------- TAB 1: RECRUITER MODE ----------------
with tab1:
    st.markdown("""
    <div class="recruiter-welcome">
        <h2 style="margin-top:0; color:#58a6ff;">Welcome, HR & Recruiters!</h2>
        <p><strong>WHAT THIS IS:</strong><br>This is a simulation of a rigid, legacy Applicant Tracking System (ATS)—the exact kind of architecture still actively filtering candidates at major corporations today.</p>
        <p><strong>WHY I BUILT THIS:</strong><br>To demonstrate my backend engineering skills and show exactly why perfectly good resumes get auto-rejected by corporate systems simply because of formatting or missing exact keywords.</p>
        <p><strong>HOW IT WORKS:</strong><br>Click the simulation button below to see how a rigid database completely destroys a modern two-column resume design. Then, head over to the <strong>Live ATS Analysis Pipeline</strong> tab to test a real resume!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Legacy ATS Parsing Simulation")
    st.markdown("Run a simulated legacy ATS parse to see how a multi-column resume can become corrupted during extraction.")
    
    if st.button("Trigger Pipeline Failure Simulation", type="secondary"):
        with st.spinner("Running ATS simulation..."):

            mock_data = {
                "status": "rejected",
                "score": 32,
                "feedback": (
                    "CRITICAL MINIMUM THRESHOLD FAILURE: Left-hand layout column collided with right-hand headers. "
                    "Extracted keywords mapped 'Languages' into 'Project Timelines'. "
                    "Parsing matrix failed to detect chronological progression. "
                    "System profile flagged as un-indexable."
                ),
                "raw_text": (
                    "MohammedZainEDUCATION"
                    "mdzain0026@email.comPROJECTS"
                    "CGPA:8.0SpeechDrivenNLU"
                    "SKILLSPythonTimelineBuiltResumeChecker"
                )
            }

            st.markdown(f"""
            <div class="score-banner">
                <h2 style="margin:0; color:#ff7b72;">Simulated Profile Score: {mock_data['score']}/100</h2>
                <p style="margin:5px 0 0 0; color:#ff7b72; font-size:18px;">
                    <strong>Status:</strong> Rejected - Formatting Error
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### Why did it fail?")

            st.markdown(
                "The old system cannot read multi-column layouts. It flattened unrelated sections into a single stream of text, making important information impossible to interpret correctly."
            )

            st.markdown("**What the database actually sees:**")

            st.markdown(
                f'<div class="correction-terminal">{mock_data["raw_text"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown("**System Error Log:**")

            st.markdown(
                f'<div class="correction-terminal" style="color:#ff7b72;">{mock_data["feedback"]}</div>',
                unsafe_allow_html=True
            )

# ---------------- TAB 2: LIVE ATS SCANNER ----------------
with tab2:
    st.markdown("### Live Keyword Match Processing")
    st.caption("First analysis may take up to 60 seconds if the demo backend is inactive.")
    st.markdown("Upload a technical resume and paste the target job requirements to see what keywords are missing and get an automated correction.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Technical Resume (PDF format)", type=["pdf"], key="live_pdf")
        job_desc = st.text_area("Target Job Profile Requirements / Keywords", height=230, placeholder="Paste job description requirements here...", key="live_jd")

    with col2:
        st.markdown("#### Analysis Engine Output")
        if uploaded_file is not None and job_desc:
            if st.button("Run System Scan", type="primary"):
                if not api_key:
                    st.error("SYSTEM HALTED: Please provide an API key in the sidebar.")
                else:
                    with st.spinner("Executing algorithms..."):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                            data = {"api_key": api_key, "job_description": job_desc}
                            
                            response = requests.post("http://127.0.0.1:8000/analyze".strip(), files=files, data=data)
                            
                            if response.status_code == 200:
                                res = response.json()
                                score = res.get("score", 0)
                                feedback = res.get("feedback", "")
                                found = res.get("found_keywords", [])
                                missing = res.get("missing_keywords", [])
                                correction = res.get("optimized_corrections", "")
                                
                                banner_class = "score-banner pass-banner" if score >= 90 else "score-banner"
                                color = "#238636" if score >= 90 else "#ff7b72"
                                status_text = "PASS: Indexed" if score >= 90 else "FAIL: Rejected"
                                
                                st.markdown(f"""
                                <div class="{banner_class}">
                                    <h1 style="margin:0; color:{color}; font-size:42px;">{score} / 100</h1>
                                    <p style="margin:5px 0 15px 0; font-weight:bold; font-size: 20px; color:{color};">{status_text}</p>
                                    <p style="margin:0; font-size: 16px; color:#c9d1d9; line-height: 1.5;"><strong>Parser Response:</strong> {feedback}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown("**Matched Keywords:**")
                                if found:
                                    st.markdown("".join([f'<span class="keyword-tag tag-found">{f}</span>' for f in found]), unsafe_allow_html=True)
                                else:
                                    st.caption("No matches found.")
                                    
                                st.markdown("<br>**Missing Keywords (Fix Immediately):**", unsafe_allow_html=True)
                                if missing:
                                    st.markdown("".join([f'<span class="keyword-tag tag-missing">{m}</span>' for m in missing]), unsafe_allow_html=True)
                                elif score < 90:
                                    st.warning("System penalized formatting or structure. No explicit missing targets extracted.")
                                else:
                                    st.success("All targets located.")
                                    
                                st.markdown("### Automated Corrections")
                                st.markdown("Replace your resume sections with this rewritten text to pass the scan:")
                                if correction:
                                    st.markdown(f'<div class="correction-terminal">{correction}</div>', unsafe_allow_html=True)
                                else:
                                    st.error("No correction data generated by the LLM. Please retry.")
                            else:
                                st.error(f"Error Code: {response.status_code}")
                        except Exception as e:
                            st.error(f"Connection failed: {str(e)}")
        else:
            st.info("Upload a document and paste job requirements to begin.")

# 5. The Footer
st.markdown("""
    <div class="footer">
        Built with ❤️ by Zain for the college students who don't want to pay to check their REAL ATS scores and get improvement advice.
    </div>
""", unsafe_allow_html=True)