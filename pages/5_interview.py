import time
import streamlit as st

from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

from ai.interview_ai import generate_questions
from ai.groq_client import transcribe_audio
from ai.voice_analysis import analyze_voice

from database.interview_db import create_interview
from database.answer_db import save_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="💼",
    layout="wide"
)

load_css()
show_sidebar()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💼 AI Mock Interview")

st.caption(
    "Answer every question carefully. AI will evaluate your performance."
)

st.divider()


# --------------------------------------------------
# LOGIN CHECK
# --------------------------------------------------

if "user" not in st.session_state:
    st.error("Please login first.")
    st.stop()


# --------------------------------------------------
# SKILLS CHECK
# --------------------------------------------------

if "skills" not in st.session_state:
    st.warning("Please upload your resume first.")
    st.stop()


# --------------------------------------------------
# GENERATE QUESTIONS
# --------------------------------------------------

if "questions" not in st.session_state:

    skills = st.session_state["skills"]

    with st.spinner("🤖 AI is preparing your interview..."):

        st.session_state["questions"] = generate_questions(skills)


# Keep only 10 questions
questions = st.session_state["questions"][:10]

st.session_state["questions"] = questions


# --------------------------------------------------
# CURRENT QUESTION
# --------------------------------------------------

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0


# --------------------------------------------------
# ANSWERS
# --------------------------------------------------

if "answers" not in st.session_state:
    st.session_state["answers"] = [""] * len(questions)


# --------------------------------------------------
# VOICE ANALYSIS FOR EACH QUESTION
# --------------------------------------------------

if "voice_analyses" not in st.session_state:
    st.session_state["voice_analyses"] = [None] * len(questions)


# --------------------------------------------------
# TIMER
# --------------------------------------------------

if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()


# --------------------------------------------------
# CREATE INTERVIEW
# --------------------------------------------------

if "interview_id" not in st.session_state:

    user = st.session_state["user"]

    st.session_state["interview_id"] = create_interview(
        user["user_id"],
        len(questions)
    )


# --------------------------------------------------
# SUBMISSION STATUS
# --------------------------------------------------

if "interview_submitted" not in st.session_state:
    st.session_state["interview_submitted"] = False


# --------------------------------------------------
# SUBMIT INTERVIEW
# --------------------------------------------------

def submit_interview():

    if st.session_state["interview_submitted"]:
        return

    interview_id = st.session_state["interview_id"]

    for i in range(len(questions)):

        save_answer(
            interview_id,
            questions[i]["question"],
            st.session_state["answers"][i],
            st.session_state["voice_analyses"][i]
        )

    st.session_state["interview_submitted"] = True
    st.session_state["interview_completed"] = True

    st.switch_page("pages/6_results.py")


# --------------------------------------------------
# QUESTION INFORMATION
# --------------------------------------------------

index = st.session_state["current_question"]

total = len(questions)

progress = (index + 1) / total


# --------------------------------------------------
# PROGRESS
# --------------------------------------------------

st.progress(progress)

st.success(
    f"📋 Question {index + 1} of {total} "
    f"({int(progress * 100)}% Completed)"
)


# --------------------------------------------------
# TIMER DISPLAY
# --------------------------------------------------

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


# --------------------------------------------------
# AUTO SUBMIT
# --------------------------------------------------

if remaining == 0:

    submit_interview()
    st.stop()


# --------------------------------------------------
# DISPLAY QUESTION
# --------------------------------------------------

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


# --------------------------------------------------
# TEXT ANSWER
# --------------------------------------------------

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


# --------------------------------------------------
# VOICE ANSWER
# --------------------------------------------------

st.divider()

st.subheader("🎙️ Voice Answer")

st.caption(
    "Record your answer and convert your voice into text using AI."
)


audio = st.audio_input(
    "🎙️ Record your answer"
)


# --------------------------------------------------
# CONVERT VOICE TO TEXT + ANALYZE VOICE
# --------------------------------------------------

if audio is not None:

    st.audio(audio)

    if st.button(
        "📝 Convert Voice to Text",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 Converting and analyzing your voice..."
        ):

            try:

                # Speech to Text
                transcript = transcribe_audio(audio)

                # Voice Analysis
                voice_result = analyze_voice(
                    audio,
                    transcript
                )

                # Store temporarily
                st.session_state["voice_transcript"] = transcript

                st.session_state["voice_analysis"] = voice_result

                st.success(
                    "✅ Voice converted and analyzed successfully!"
                )

            except Exception as e:

                st.error(
                    f"Voice conversion failed: {e}"
                )


# --------------------------------------------------
# DISPLAY TRANSCRIPT
# --------------------------------------------------

if "voice_transcript" in st.session_state:

    st.subheader("📝 Transcribed Answer")

    st.text_area(
        "AI Transcription",
        value=st.session_state["voice_transcript"],
        height=200,
        disabled=True
    )


# --------------------------------------------------
# DISPLAY VOICE ANALYSIS
# --------------------------------------------------

if "voice_analysis" in st.session_state:

    result = st.session_state["voice_analysis"]

    if "error" not in result:

        st.divider()

        st.subheader("🎙️ Voice Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Speaking Pace",
                result["speaking_pace"]
            )

        with col2:

            st.metric(
                "Pauses",
                result["pause_count"]
            )

        with col3:

            st.metric(
                "Voice Energy",
                f'{result["voice_energy"]}%'
            )

        st.metric(
            "Confidence Indicator",
            f'{result["confidence_indicator"]}%'
        )

        st.caption(
            "The confidence indicator is an estimate based "
            "on speaking pace, pauses, silence and voice energy."
        )


# --------------------------------------------------
# USE VOICE ANSWER
# --------------------------------------------------

if "voice_transcript" in st.session_state:

    if st.button(
        "📥 Use This Answer",
        use_container_width=True
    ):

        transcript = st.session_state["voice_transcript"]

        # Save transcript
        st.session_state["answers"][index] = transcript

        # Save voice analysis for THIS question
        if "voice_analysis" in st.session_state:

            result = st.session_state["voice_analysis"]

            if "error" not in result:

                st.session_state["voice_analyses"][index] = result

        # Remove temporary data
        del st.session_state["voice_transcript"]

        if "voice_analysis" in st.session_state:
            del st.session_state["voice_analysis"]

        # Remove old text widget value
        # so the transcript appears in the text area
        if text_key in st.session_state:
            del st.session_state[text_key]

        st.success(
            "✅ Voice answer added successfully!"
        )

        st.rerun()


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


# --------------------------------------------------
# PREVIOUS
# --------------------------------------------------

with col1:

    if st.button(
        "⬅ Previous",
        use_container_width=True
    ):

        if index > 0:

            st.session_state["answers"][index] = (
                st.session_state[text_key]
            )

            # Clear temporary voice data
            if "voice_transcript" in st.session_state:
                del st.session_state["voice_transcript"]

            if "voice_analysis" in st.session_state:
                del st.session_state["voice_analysis"]

            st.session_state["current_question"] -= 1

            st.rerun()


# --------------------------------------------------
# NEXT
# --------------------------------------------------

with col2:

    if index < total - 1:

        if st.button(
            "Next ➡",
            use_container_width=True
        ):

            st.session_state["answers"][index] = (
                st.session_state[text_key]
            )

            # Clear temporary voice data
            if "voice_transcript" in st.session_state:
                del st.session_state["voice_transcript"]

            if "voice_analysis" in st.session_state:
                del st.session_state["voice_analysis"]

            st.session_state["current_question"] += 1

            st.rerun()


# --------------------------------------------------
# SUBMIT
# --------------------------------------------------

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


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

show_footer()
