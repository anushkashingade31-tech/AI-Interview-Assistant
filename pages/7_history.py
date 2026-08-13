import streamlit as st

from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from database.interview_db import get_interview_history

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Interview History",
    page_icon="📚",
    layout="wide"
)

load_css()
show_sidebar()

st.title("📚 Interview History")

st.caption(
    "View all your previous AI mock interviews."
)

st.divider()

# --------------------------------------------------
# Login Check
# --------------------------------------------------

if "user" not in st.session_state:

    st.warning("Please login first.")

    st.stop()

user = st.session_state["user"]

# --------------------------------------------------
# Fetch Interview History
# --------------------------------------------------

history = get_interview_history(
    user["user_id"]
)

if len(history) == 0:

    st.info("No interview history found.")

    show_footer()

    st.stop()

# Latest interview first
history.reverse()

# --------------------------------------------------
# Statistics
# --------------------------------------------------

st.success(
    f"🎤 Total Interviews: {len(history)}"
)

st.divider()

# --------------------------------------------------
# Display Interview History
# --------------------------------------------------

for index, interview in enumerate(history, start=1):

    score = interview["overall_score"]

    if score is None:
        score = 0

    with st.container(border=True):

        st.subheader(f"🎤 Interview #{index}")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"📅 **Date:** {interview['interview_date']}"
            )

            st.write(
                f"📝 **Total Questions:** {interview['total_questions']}"
            )

        with col2:

            st.metric(
                "⭐ Overall Score",
                f"{score:.1f}/10"
            )

        # ------------------------------------
        # Performance Badge
        # ------------------------------------

        if score >= 9:

            st.success("🌟 Excellent Performance")

        elif score >= 7:

            st.success("✅ Very Good Performance")

        elif score >= 5:

            st.warning("👍 Good Performance")

        else:

            st.error("📚 Needs More Practice")

        # ------------------------------------
        # View Details Button
        # ------------------------------------

        if st.button(
            "📄 View Details",
            key=f"view_{interview['interview_id']}",
            use_container_width=True
        ):

            st.session_state["selected_interview"] = interview["interview_id"]

            st.switch_page(
                "pages/6_results.py"
            )

# --------------------------------------------------
# Bottom Navigation
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_dashboard.py"
        )

with col2:

    if st.button(
        "🎤 New Interview",
        use_container_width=True
    ):

        # Clear previous interview session

        for key in [

            "questions",
            "answers",
            "current_question",
            "start_time",
            "interview_id",
            "interview_completed",
            "selected_interview"

        ]:

            st.session_state.pop(key, None)

        st.switch_page(
            "pages/4_resume.py"
        )

show_footer()
