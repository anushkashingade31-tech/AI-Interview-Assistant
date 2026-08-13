import streamlit as st

from ai.evaluator import evaluate_answer
from utils.pdf_generator import generate_pdf
from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from database.answer_db import (
    get_answers,
    update_answer_evaluation
)

from database.interview_db import (
    update_overall_score
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Interview Results",
    page_icon="📊",
    layout="wide"
)

load_css()
show_sidebar()

# --------------------------------------------------
# Success Animation
# --------------------------------------------------

st.balloons()

st.success("🎉 Interview Completed Successfully!")

st.title("📊 AI Interview Results")

st.caption(
    "Your interview has been evaluated using AI."
)

st.divider()

# --------------------------------------------------
# Check Interview
# --------------------------------------------------

if "interview_id" not in st.session_state:

    st.error("No interview found.")

    st.stop()

if "selected_interview" in st.session_state:

    interview_id = st.session_state["selected_interview"]

else:

    interview_id = st.session_state["interview_id"]

answers = get_answers(interview_id)

if len(answers) == 0:

    st.warning("No answers found.")

    st.stop()

# --------------------------------------------------
# Evaluate Answers
# --------------------------------------------------

total_score = 0

for i, answer in enumerate(answers):

    st.divider()

    st.subheader(f"📝 Question {i + 1}")

    st.info(answer["question"])

    st.subheader("✍ Your Answer")

    st.write(answer["user_answer"])

    # ------------------------------
    # AI Evaluation
    # ------------------------------

    if answer["ai_score"] is None:

        with st.spinner("🤖 AI is evaluating your answer..."):

            result = evaluate_answer(

                answer["question"],

                answer["user_answer"]

            )

            update_answer_evaluation(

                answer["answer_id"],

                result["score"],

                result["feedback"],

                result["ideal_answer"]

            )

            answer["ai_score"] = result["score"]

            answer["feedback"] = result["feedback"]

            answer["ideal_answer"] = result["ideal_answer"]

    score = float(answer["ai_score"])

    total_score += score

    # ------------------------------
    # Score Color
    # ------------------------------

    if score >= 8:

        st.success(f"🌟 AI Score : {score}/10")

    elif score >= 5:

        st.warning(f"⭐ AI Score : {score}/10")

    else:

        st.error(f"📚 AI Score : {score}/10")

    st.subheader("💬 AI Feedback")

    st.info(answer["feedback"])

    with st.expander("📖 View Ideal Answer"):

        st.success(answer["ideal_answer"])

# --------------------------------------------------
# Overall Performance
# --------------------------------------------------

average_score = total_score / len(answers)

update_overall_score(

    interview_id,

    average_score

)

percentage = average_score * 10

st.divider()

st.header("🏆 Overall Performance")

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Average Score",

        f"{average_score:.1f}/10"

    )

with col2:

    st.metric(

        "Percentage",

        f"{percentage:.1f}%"

    )

st.progress(percentage / 100)

# --------------------------------------------------
# Performance Rating
# --------------------------------------------------

if average_score >= 9:

    st.success("🌟 Excellent Performance")

elif average_score >= 7:

    st.success("✅ Very Good Performance")

elif average_score >= 5:

    st.warning("👍 Good Performance")

else:

    st.error("📚 Needs More Practice")

# --------------------------------------------------
# Generate PDF
# --------------------------------------------------

user = st.session_state["user"]

pdf_path = "Interview_Report.pdf"

generate_pdf(

    user["full_name"],

    answers,

    average_score,

    pdf_path

)

with open(pdf_path, "rb") as file:

    st.download_button(

        "📄 Download Interview Report",

        file,

        file_name="Interview_Report.pdf",

        mime="application/pdf",

        use_container_width=True

    )

# --------------------------------------------------
# Navigation
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(

        "📚 View History",

        use_container_width=True

    ):

        st.switch_page(

            "pages/7_history.py"

        )

with col2:

    if st.button(

        "🏠 Dashboard",

        use_container_width=True

    ):

        st.switch_page(

            "pages/3_dashboard.py"

        )

show_footer()