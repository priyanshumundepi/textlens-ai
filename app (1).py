import streamlit as st
from google import genai
from datetime import datetime

st.set_page_config(
    page_title="TextLens AI",
    page_icon="🔎",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #10172d);
    color: #f1f5f9;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #172554, #312e81, #4c1d95);
    padding: 30px;
    border: 1px solid #4338ca;
    border-radius: 20px;
    margin-bottom: 24px;
}
.hero h1 { color: white; font-size: 38px; }
.hero p { color: #dbeafe; }
.panel {
    background: #151e33;
    border: 1px solid #293651;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
}
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 600;
}
[data-testid="stSidebar"] {
    background: #0d1426;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🔎 TextLens AI")
    st.caption("Generative AI Project")
    st.divider()
    st.markdown("🏠 Text Analysis")
    st.markdown("📊 Writing Insights")
    st.markdown("📄 Report Export")
    st.divider()
    st.caption("Built with Streamlit + Gemini API")
    st.caption("BTech CSE Project")

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>TextLens AI 🔎</h1>
    <p>Explore writing patterns with AI-assisted text analysis.</p>
</div>
""", unsafe_allow_html=True)

st.info(
    "Writing-style analysis cannot reliably prove whether "
    "text was written by AI or a human."
)

# ---------- INPUT ----------
st.subheader("📝 Analyse Your Text")

api_key = st.text_input(
    "Gemini API key",
    type="password",
    help="Your key is used for the current session. Never share it."
)

text = st.text_area(
    "Paste your text here",
    height=200,
    placeholder="Enter at least 20 characters..."
)

words = len(text.split())
characters = len(text)

c1, c2, c3 = st.columns(3)
c1.metric("Words", words)
c2.metric("Characters", characters)
c3.metric("Minimum length", "20 characters")

# ---------- ANALYSE ----------
if st.button("🔍 Analyse Writing", use_container_width=True):
    if not api_key.strip():
        st.warning("Please enter your Gemini API key.")
    elif len(text.strip()) < 20:
        st.warning("Please enter at least 20 characters.")
    else:
        try:
            client = genai.Client(api_key=api_key.strip())

            prompt = f"""
Analyse the writing style of the text below.

Include:
1. Writing style
2. Sentence structure
3. Repetition or predictable patterns
4. Features sometimes associated with AI-assisted writing
5. Features sometimes associated with human writing
6. A cautious overall assessment
7. A short explanation

Do not give a numerical AI probability.
Do not claim writing style proves authorship.
Mention that human and AI writing can overlap.

TEXT:
{text}
"""

            with st.spinner("Analysing writing patterns..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            st.session_state["analysis_result"] = response.text
            st.session_state["analysed_text"] = text
            st.session_state["analysis_date"] = (
                datetime.now().strftime("%Y-%m-%d %H:%M")
            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")

# ---------- RESULTS & DOWNLOAD ----------
if st.session_state.get("analysis_result"):
    result = st.session_state["analysis_result"]
    analysed_text = st.session_state["analysed_text"]
    analysis_date = st.session_state["analysis_date"]

    st.divider()
    st.subheader("📊 Analysis Results")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption(
        "This is a qualitative, model-generated assessment, "
        "not a validated AI-authorship detector."
    )

    report = f"""TEXTLENS AI
Writing Style Analysis Report
========================================

Date: {analysis_date}

TEXT ANALYSED:
{analysed_text}

ANALYSIS:
{result}

DISCLAIMER:
This report does not prove whether a text was written
by a human or an AI system. Results are exploratory.
"""

    st.download_button(
        label="📄 Download Analysis Report",
        data=report,
        file_name="TextLens_AI_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.success("Your analysis report is ready to download!")

# ---------- FOOTER ----------
st.divider()
st.caption("TextLens AI | Generative AI Project | BTech CSE")
