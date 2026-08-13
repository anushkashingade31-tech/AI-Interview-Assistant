import time
import streamlit as st
from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from ai.interview_ai import generate_questions
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

        st.session_state["questions"] = generate_questions(
            skills
        )

# -------------------------------------
# Initialize Session
# -------------------------------------

questions = st.session_state["questions"]



if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

if "answers" not in st.session_state:
    st.session_state["answers"] = [
        ""
    ] * len(questions)

if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

if "interview_id" not in st.session_state:

    user = st.session_state["user"]

    st.session_state["interview_id"] = create_interview(
        user["user_id"],
        len(questions)
    )

index = st.session_state["current_question"]

total = len(questions)

# -------------------------------------
# Progress
# -------------------------------------

progress = (index + 1) / total

st.progress(progress)

st.success(
    f"📋 Question {index + 1} of {total} "
    f"({int(progress*100)}% Completed)"
)

# -------------------------------------
# Timer
# -------------------------------------

elapsed = int(
    time.time()
    -
    st.session_state["start_time"]
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
if remaining == 0:

    interview_id = st.session_state["interview_id"]

    for i in range(len(questions)):
        st.write("Saving:", questions[i]["question"])
        st.write("Answer:", st.session_state["answers"][i])

        save_answer(

            interview_id,

            questions[i]["question"],

            st.session_state["answers"][i]

        )
        st.success("Saved successfully")

    st.session_state["interview_completed"] = True

    st.switch_page("pages/6_results.py")

# -------------------------------------
# Current Question
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

# Unique key for each question
text_key = f"answer_{index}"

# Initialize only once
if text_key not in st.session_state:
    st.session_state[text_key] = st.session_state["answers"][index]

# Text area
st.text_area(
    "✍ Your Answer",
    key=text_key,
    height=260,
    placeholder="Type your answer here..."
)

# Save latest answer
st.session_state["answers"][index] = st.session_state[text_key]
# -------------------------------------
# Navigation
# -------------------------------------

col1, col2, col3 = st.columns([1,1,1])

with col1:

    if st.button(
        "⬅ Previous",
        use_container_width=True
    ):

        if index > 0:

            st.session_state["answers"][index] = st.session_state[text_key]

            st.session_state["current_question"] -= 1

            st.rerun()


with col2:

    if index < total - 1:

        if st.button(
            "Next ➡",
            use_container_width=True
        ):

            st.session_state["answers"][index] = st.session_state[text_key]

            st.session_state["current_question"] += 1

            st.rerun()


with col3:

    if index == total - 1:

        if st.button(
            "✅ Submit Interview",
            use_container_width=True
        ):

            st.session_state["answers"][index] = st.session_state[text_key]

            interview_id = st.session_state["interview_id"]

            for i in range(len(questions)):

                save_answer(

                    interview_id,

                    questions[i]["question"],

                    st.session_state["answers"][i]

                )

            st.session_state["interview_completed"] = True

            st.switch_page("pages/6_results.py")
show_footer()
