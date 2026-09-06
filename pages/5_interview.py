import time
import streamlit as st

from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from ai.interview_ai import generate_questions
from ai.groq_client import transcribe_audio

from database.interview_db import create_interview
from database.answer_db import save_answer


st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="💼",
    layout="wide"
)

load_css()
show_sidebar()

st.title("💼 AI Mock Interview")

st.caption(
    "Answer every question carefully. AI will evaluate your performance."
)

st.divider()


# -------------------------------------
# Login Check
# -------------------------------------

if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()


# -------------------------------------
# Resume Check
# -------------------------------------

if "skills" not in st.session_state:
    st.warning("Please upload your resume first.")
    st.stop()


# -------------------------------------
# Generate Questions Only Once
# -------------------------------------

if "questions" not in st.session_state:

    skills = st.session_state["skills"]

    with st.spinner("🤖 AI is preparing your interview..."):

        st.session_state["questions"] = generate_questions(skills)


questions = st.session_state["questions"]


# -------------------------------------
# Initialize Interview
# -------------------------------------

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0


if "answers" not in st.session_state:
    st.session_state["answers"] = [""] * len(questions)


if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()


if "interview_id" not in st.session_state:

    user = st.session_state["user"]

    st.session_state["interview_id"] = create_interview(
        user["user_id"],
        len(questions)
    )


# -------------------------------------
# Prevent Duplicate Submission
# -------------------------------------

if "interview_submitted" not in st.session_state:
    st.session_state["interview_submitted"] = False


# -------------------------------------
# Submit Function
# -------------------------------------

def submit_interview():

    if st.session_state["interview_submitted"]:
        return

    interview_id = st.session_state["interview_id"]

    for i in range(len(questions)):

        save_answer(
            interview_id,
            questions[i]["question"],
            st.session_state["answers"][i]
        )

    st.session_state["interview_submitted"] = True
    st.session_state["interview_completed"] = True

    st.switch_page("pages/6_results.py")


# -------------------------------------
# Current Question
# -------------------------------------

index = st.session_state["current_question"]

total = len(questions)


# -------------------------------------
# Progress
# -------------------------------------

progress = (index + 1) / total

st.progress(progress)

st.success(
    f"📋 Question {index + 1} of {total} "
    f"({int(progress * 100)}% Completed)"
)


# -------------------------------------
# Timer
# -------------------------------------

elapsed = int(
    time.time() - st.session_state["start_time"]
)

remaining = max(
    0,
    600 - elapsed
)

minutes = remaining // 60
seconds = remaining % 60


if remaining > 300:

    st.success(
        f"⏰ Time Remaining : {minutes:02d}:{seconds:02d}"
    )

elif remaining > 120:

    st.warning(
        f"⚠️ Time Remaining : {minutes:02d}:{seconds:02d}"
    )

else:

    st.error(
        f"🚨 Time Remaining : {minutes:02d}:{seconds:02d}"
    )


# -------------------------------------
# Automatic Submission
# -------------------------------------

if remaining == 0:

    submit_interview()

    st.stop()


# -------------------------------------
# Display Current Question
# -------------------------------------

question = questions[index]

st.subheader(f"📝 Question {index + 1}")

st.markdown(
    f"""
### {question['question']}

**💡 Skill:** {question['skill']}

**⭐ Difficulty:** {question['difficulty']}
"""
)

st.divider()


# -------------------------------------
# Text Answer
# -------------------------------------

text_key = f"answer_{index}"


if text_key not in st.session_state:

    st.session_state[text_key] = (
        st.session_state["answers"][index]
    )


st.text_area(
    "✍ Your Answer",
    key=text_key,
    height=260,
    placeholder="Type your answer here..."
)


# Save text answer
st.session_state["answers"][index] = (
    st.session_state[text_key]
)


st.divider()


# -------------------------------------
# Voice Answer
# -------------------------------------

st.subheader("🎙️ Voice Answer")

st.caption(
    "You can record your answer and convert it into text using AI."
)

audio = st.audio_input(
    "🎙️ Record your answer"
)


if audio is not None:

    st.audio(audio)

    if st.button(
        "📝 Convert Voice to Text",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 Converting your voice to text..."
        ):

            try:

                transcript = transcribe_audio(audio)

                st.session_state[text_key] = transcript

                st.session_state["answers"][index] = transcript

                st.success(
                    "✅ Voice converted to text successfully!"
                )

                st.text_area(
                    "📝 Transcribed Answer",
                    value=transcript,
                    height=200
                )

            except Exception as e:

                st.error(
                    f"Voice conversion failed: {e}"
                )


st.divider()


# -------------------------------------
# Navigation
# -------------------------------------

col1, col2, col3 = st.columns(3)


# Previous
with col1:

    if st.button(
        "⬅ Previous",
        use_container_width=True
    ):

        if index > 0:

            st.session_state["answers"][index] = (
                st.session_state[text_key]
            )

            st.session_state["current_question"] -= 1

            st.rerun()


# Next
with col2:

    if index < total - 1:

        if st.button(
            "Next ➡",
            use_container_width=True
        ):

            st.session_state["answers"][index] = (
                st.session_state[text_key]
            )

            st.session_state["current_question"] += 1

            st.rerun()


# Submit
with col3:

    if index == total - 1:

        if st.button(
            "✅ Submit Interview",
            use_container_width=True
        ):

            st.session_state["answers"][index] = (
                st.session_state[text_key]
            )

            submit_interview()


show_footer()
