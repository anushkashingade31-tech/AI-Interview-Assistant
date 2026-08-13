import streamlit as st

# MUST be first Streamlit command
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

load_css()
show_sidebar()

# -----------------------------
# Already Logged In?
# -----------------------------

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.switch_page("pages/3_dashboard.py")

# -----------------------------
# Home Page
# -----------------------------

st.title("🤖 AI Interview Preparation Assistant")

st.markdown("""
### Welcome!

Prepare for interviews using Artificial Intelligence.

### Features

- 📄 Resume Upload
- 🧠 AI Resume Analysis
- 💼 AI Question Generation
- 🎤 Mock Interview
- 📊 Performance Analysis
- 📚 Interview History
- 📄 PDF Report

---

### Tech Stack

- Python
- Streamlit
- MySQL
- Groq AI

---

Use the sidebar to **Register** or **Login**.
""")

show_footer()