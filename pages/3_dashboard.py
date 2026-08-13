import streamlit as st

# ---------------------------------
# Page Configuration (Must be first)
# ---------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from database.interview_db import (
    get_total_interviews,
    get_average_score,
    get_highest_score
)

load_css()
show_sidebar()

# ---------------------------------
# Login Check
# ---------------------------------

if (
    "logged_in" not in st.session_state
    or
    "user" not in st.session_state
):

    st.warning("Please login first.")

    st.switch_page("pages/1_login.py")

    st.stop()

user = st.session_state["user"]

# ---------------------------------
# Dashboard Statistics
# ---------------------------------

total_interviews = get_total_interviews(
    user["user_id"]
)

average_score = get_average_score(
    user["user_id"]
)

highest_score = get_highest_score(
    user["user_id"]
)

# ---------------------------------
# Dashboard
# ---------------------------------

st.title("🤖 AI Interview Preparation Assistant")

st.caption(
    "Practice technical interviews with AI-powered feedback."
)

st.write(f"## Welcome, {user['full_name']} 👋")

st.divider()

# ---------------------------------
# Statistics
# ---------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🎤 Total Interviews",
        total_interviews
    )

with col2:

    st.metric(
        "📈 Average Score",
        f"{average_score}/10"
    )

with col3:

    st.metric(
        "🏆 Highest Score",
        f"{highest_score}/10"
    )

st.divider()

# ---------------------------------
# Recent Activity
# ---------------------------------

st.subheader("📌 Recent Activity")

if total_interviews == 0:

    st.info(
        "No interviews completed yet."
    )

else:

    st.success(
        f"You have completed {total_interviews} interview(s)."
    )

st.divider()

# ---------------------------------
# Quick Actions
# ---------------------------------

st.subheader("🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "📄 Upload Resume",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_resume.py"
        )

with col2:

    if st.button(
        "🎤 Start Interview",
        use_container_width=True
    ):

        st.switch_page(
            "pages/5_interview.py"
        )

with col3:

    if st.button(
        "📊 Results",
        use_container_width=True
    ):

        st.switch_page(
            "pages/6_results.py"
        )

with col4:

    if st.button(
        "📚 History",
        use_container_width=True
    ):

        st.switch_page(
            "pages/7_history.py"
        )

st.divider()

# ---------------------------------
# Logout
# ---------------------------------

if st.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.clear()

    st.switch_page("app.py")

show_footer()