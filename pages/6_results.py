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
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Interview Results",
    page_icon="📊",
    layout="wide"
)

load_css()
show_sidebar()


# --------------------------------------------------
# SUCCESS MESSAGE
# --------------------------------------------------

st.balloons()

st.success(
    "🎉 Interview Completed Successfully!"
)

st.title("📊 AI Interview Results")

st.caption(
    "Your interview has been evaluated using AI."
)

st.divider()


# --------------------------------------------------
# CHECK INTERVIEW
# --------------------------------------------------

if "interview_id" not in st.session_state:

    st.error("No interview found.")

    st.stop()


if "selected_interview" in st.session_state:

    interview_id = st.session_state["selected_interview"]

else:

    interview_id = st.session_state["interview_id"]


# --------------------------------------------------
# GET ANSWERS
# --------------------------------------------------

answers = get_answers(interview_id)


if len(answers) == 0:

    st.warning("No answers found.")

    st.stop()


# --------------------------------------------------
# EVALUATE ANSWERS
# --------------------------------------------------

total_score = 0


for i, answer in enumerate(answers):

    st.divider()

    # --------------------------------------------------
    # QUESTION
    # --------------------------------------------------

    st.subheader(
        f"📝 Question {i + 1}"
    )

    st.info(
        answer["question"]
    )


    # --------------------------------------------------
    # USER ANSWER
    # --------------------------------------------------

    st.subheader(
        "✍ Your Answer"
    )

    if (
        answer["user_answer"]
        and answer["user_answer"].strip()
    ):

        st.write(
            answer["user_answer"]
        )

    else:

        st.warning(
            "⚠️ No answer was provided."
        )


    # --------------------------------------------------
    # AI EVALUATION
    # --------------------------------------------------

    if answer["ai_score"] is None:

        user_answer = answer["user_answer"]


        # ----------------------------------------------
        # EMPTY ANSWER
        # ----------------------------------------------

        if (
            not user_answer
            or not user_answer.strip()
        ):

            result = {

                "score": 0,

                "feedback": (
                    "No answer was provided "
                    "for this question."
                ),

                "ideal_answer": (
                    "Please provide an answer "
                    "to the question."
                )

            }


        # ----------------------------------------------
        # ANSWER PROVIDED
        # ----------------------------------------------

        else:

            with st.spinner(
                "🤖 AI is evaluating your answer..."
            ):

                result = evaluate_answer(
                    answer["question"],
                    user_answer
                )


        # ----------------------------------------------
        # SAVE EVALUATION
        # ----------------------------------------------

        update_answer_evaluation(
            answer["answer_id"],
            result["score"],
            result["feedback"],
            result["ideal_answer"]
        )


        # Update current answer
        answer["ai_score"] = result["score"]

        answer["feedback"] = result["feedback"]

        answer["ideal_answer"] = result["ideal_answer"]


    # --------------------------------------------------
    # SCORE
    # --------------------------------------------------

    score = float(
        answer["ai_score"]
    )

    total_score += score


    # --------------------------------------------------
    # SCORE DISPLAY
    # --------------------------------------------------

    if score >= 8:

        st.success(
            f"🌟 AI Score : {score}/10"
        )

    elif score >= 5:

        st.warning(
            f"⭐ AI Score : {score}/10"
        )

    else:

        st.error(
            f"📚 AI Score : {score}/10"
        )


    # --------------------------------------------------
    # AI FEEDBACK
    # --------------------------------------------------

    st.subheader(
        "💬 AI Feedback"
    )

    st.info(
        answer["feedback"]
    )


    # --------------------------------------------------
    # IDEAL ANSWER
    # --------------------------------------------------

    with st.expander(
        "📖 View Ideal Answer"
    ):

        st.success(
            answer["ideal_answer"]
        )


    # ==================================================
    # VOICE ANALYSIS
    # ==================================================

    confidence = answer.get(
        "confidence_indicator"
    )

    if confidence is not None:

        st.divider()

        st.subheader(
            "🎙️ Voice Analysis"
        )

        st.caption(
            "Voice analysis provides indicators based "
            "on speaking pace, pauses, silence and "
            "voice energy."
        )


        # ----------------------------------------------
        # ROW 1
        # ----------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            wpm = answer.get(
                "words_per_minute"
            )

            if wpm is not None:

                st.metric(
                    "Speaking Pace",
                    f"{float(wpm):.1f} WPM"
                )

            else:

                st.metric(
                    "Speaking Pace",
                    "N/A"
                )


        with col2:

            pause_count = answer.get(
                "pause_count"
            )

            if pause_count is not None:

                st.metric(
                    "Pauses",
                    int(pause_count)
                )

            else:

                st.metric(
                    "Pauses",
                    "N/A"
                )


        with col3:

            voice_energy = answer.get(
                "voice_energy"
            )

            if voice_energy is not None:

                st.metric(
                    "Voice Energy",
                    f"{int(voice_energy)}%"
                )

            else:

                st.metric(
                    "Voice Energy",
                    "N/A"
                )


        # ----------------------------------------------
        # ROW 2
        # ----------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            duration = answer.get(
                "voice_duration"
            )

            if duration is not None:

                st.metric(
                    "Duration",
                    f"{float(duration):.1f} sec"
                )

            else:

                st.metric(
                    "Duration",
                    "N/A"
                )


        with col2:

            silence = answer.get(
                "silence_percentage"
            )

            if silence is not None:

                st.metric(
                    "Silence",
                    f"{float(silence):.1f}%"
                )

            else:

                st.metric(
                    "Silence",
                    "N/A"
                )


        with col3:

            st.metric(
                "Confidence Indicator",
                f"{int(confidence)}%"
            )


        # ----------------------------------------------
        # CONFIDENCE PROGRESS
        # ----------------------------------------------

        st.progress(
            max(
                0,
                min(
                    100,
                    int(confidence)
                )
            ) / 100
        )


        st.caption(
            "The confidence indicator is an estimate "
            "based on speaking pace, pauses, silence "
            "and voice energy. It does not directly "
            "measure a person's actual confidence."
        )


# ==================================================
# OVERALL PERFORMANCE
# ==================================================

average_score = (
    total_score / len(answers)
)


# --------------------------------------------------
# SAVE OVERALL SCORE
# --------------------------------------------------

update_overall_score(
    interview_id,
    average_score
)


percentage = average_score * 10


st.divider()

st.header(
    "🏆 Overall Performance"
)


# --------------------------------------------------
# SCORE METRICS
# --------------------------------------------------

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


st.progress(
    percentage / 100
)


# --------------------------------------------------
# PERFORMANCE RATING
# --------------------------------------------------

if average_score >= 9:

    st.success(
        "🌟 Excellent Performance"
    )

elif average_score >= 7:

    st.success(
        "✅ Very Good Performance"
    )

elif average_score >= 5:

    st.warning(
        "👍 Good Performance"
    )

else:

    st.error(
        "📚 Needs More Practice"
    )


# ==================================================
# OVERALL VOICE PERFORMANCE
# ==================================================

voice_answers = []

for answer in answers:

    if answer.get(
        "confidence_indicator"
    ) is not None:

        voice_answers.append(answer)


if voice_answers:

    st.divider()

    st.header(
        "🎙️ Overall Voice Performance"
    )


    # --------------------------------------------------
    # AVERAGE CONFIDENCE INDICATOR
    # --------------------------------------------------

    avg_confidence = sum(
        float(
            answer["confidence_indicator"]
        )
        for answer in voice_answers
    ) / len(voice_answers)


    # --------------------------------------------------
    # AVERAGE WPM
    # --------------------------------------------------

    valid_wpm = [
        float(answer["words_per_minute"])
        for answer in voice_answers
        if answer.get("words_per_minute") is not None
    ]


    if valid_wpm:

        avg_wpm = sum(valid_wpm) / len(valid_wpm)

    else:

        avg_wpm = 0


    # --------------------------------------------------
    # TOTAL PAUSES
    # --------------------------------------------------

    total_pauses = sum(
        int(answer["pause_count"])
        for answer in voice_answers
        if answer.get("pause_count") is not None
    )


    # --------------------------------------------------
    # DISPLAY
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Confidence Indicator",
            f"{avg_confidence:.1f}%"
        )


    with col2:

        st.metric(
            "Average Speaking Pace",
            f"{avg_wpm:.1f} WPM"
        )


    with col3:

        st.metric(
            "Total Pauses",
            total_pauses
        )


    st.progress(
        max(
            0,
            min(
                100,
                int(avg_confidence)
            )
        ) / 100
    )


    st.caption(
        "This voice score is an estimated communication "
        "indicator based on measurable audio characteristics."
    )


# ==================================================
# GENERATE PDF
# ==================================================

user = st.session_state["user"]

pdf_path = "Interview_Report.pdf"


generate_pdf(
    user["full_name"],
    answers,
    average_score,
    pdf_path
)


with open(
    pdf_path,
    "rb"
) as file:

    st.download_button(

        "📄 Download Interview Report",

        file,

        file_name="Interview_Report.pdf",

        mime="application/pdf",

        use_container_width=True
    )


# ==================================================
# NAVIGATION
# ==================================================

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


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

show_footer()
