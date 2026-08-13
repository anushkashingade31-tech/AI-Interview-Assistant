import streamlit as st

from database.user_db import get_user_by_email
from utils.auth import verify_password
from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

load_css()
show_sidebar()

# ---------------------------------------
# Title
# ---------------------------------------

st.title("🔐 Login")

st.caption("Login to continue your AI Interview Preparation Journey.")

st.divider()

# ---------------------------------------
# Login Form
# ---------------------------------------

email = st.text_input(
    "📧 Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "🔑 Password",
    type="password",
    placeholder="Enter your password"
)

st.write("")

# ---------------------------------------
# Login Button
# ---------------------------------------

st.markdown(
    '<div class="primary-btn">',
    unsafe_allow_html=True
)

if st.button(
    "🚀 Login",
    use_container_width=True
):

    if email.strip() == "" or password.strip() == "":

        st.warning("Please enter both Email and Password.")

    else:

        user = get_user_by_email(email)

        if user:

            if verify_password(password, user["password"]):

                st.session_state["logged_in"] = True
                st.session_state["user"] = user

                st.success("✅ Login Successful!")

                st.switch_page("pages/3_dashboard.py")

            else:

                st.error("❌ Incorrect Password")

        else:

            st.error("❌ User Not Found")

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

st.divider()

st.info("💡 New user? Please register first.")

show_footer()