import os
import streamlit as st

from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from ai.resume_parser import extract_text
from ai.resume_ai import analyze_resume

st.set_page_config(
    page_title="Resume Upload",
    page_icon="📄",
    layout="wide"
)

load_css()
show_sidebar()

st.title("📄 Resume Upload")
st.caption("Upload your resume and let AI analyze your skills.")

st.divider()

# ----------------------------------------
# Login Check
# ----------------------------------------

if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()

# ----------------------------------------
# Upload Folder
# ----------------------------------------

os.makedirs("uploads", exist_ok=True)

# ----------------------------------------
# Upload Resume
# ----------------------------------------

uploaded_file = st.file_uploader(
    "Choose your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully!")

    # ----------------------------------------
    # Extract Resume
    # ----------------------------------------

    with st.spinner("📄 Extracting resume text..."):
        resume_text = extract_text(file_path)

    st.success("✅ Resume text extracted!")

    # ----------------------------------------
    # AI Resume Analysis
    # ----------------------------------------

    with st.spinner("🤖 AI is analyzing your resume..."):

        try:

            result = analyze_resume(resume_text)

            st.session_state["resume"] = result
            st.session_state["skills"] = result.get("skills", [])

            st.success("🎉 Resume analyzed successfully!")

            # -----------------------------
            # Candidate Details
            # -----------------------------

            st.subheader("👤 Candidate Information")

            col1, col2 = st.columns(2)

            with col1:

                st.info(f"**Name**\n\n{result.get('name', '-')}")
                st.info(f"**Email**\n\n{result.get('email', '-')}")
                st.info(f"**Phone**\n\n{result.get('phone', '-')}")

            with col2:

                st.info(f"**Education**\n\n{result.get('education', '-')}")
                st.info(f"**Experience**\n\n{result.get('experience', '-')}")

            st.divider()

            # -----------------------------
            # Skills
            # -----------------------------

            st.subheader("💡 Extracted Skills")

            skills = result.get("skills", [])

            if skills:

                for skill in skills:
                    st.success(f"✔ {skill}")

            else:

                st.warning("No skills found.")

        except Exception as e:

            st.error(f"AI Error: {e}")

# ----------------------------------------
# Continue Button
# ----------------------------------------

if "resume" in st.session_state:

    st.divider()

    st.markdown(
        '<div class="success-btn">',
        unsafe_allow_html=True
    )

    if st.button(
        "🎤 Continue to Interview",
        use_container_width=True
    ):

        # Clear previous interview session
        keys = [
            "questions",
            "answers",
            "current_question",
            "start_time",
            "interview_id",
            "interview_completed",
            "selected_interview"
        ]

        for key in keys:
            st.session_state.pop(key, None)

        st.switch_page("pages/5_interview.py")

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

show_footer()