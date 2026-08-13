import streamlit as st

from database.user_db import create_user
from utils.auth import hash_password
from utils.style import load_css
from utils.sidebar import show_sidebar
from utils.footer import show_footer

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

load_css()
show_sidebar()

st.title("📝 Create Account")

st.caption("Create your AI Interview Assistant account.")

st.divider()

full_name = st.text_input(
    "👤 Full Name",
    placeholder="Enter your full name"
)

email = st.text_input(
    "📧 Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "🔒 Password",
    type="password",
    placeholder="Enter your password"
)

confirm_password = st.text_input(
    "🔒 Confirm Password",
    type="password",
    placeholder="Re-enter your password"
)

st.write("")

st.markdown(
    '<div class="success-btn">',
    unsafe_allow_html=True
)

if st.button(
    "✅ Register",
    use_container_width=True
):

    if (
        full_name.strip() == "" or
        email.strip() == "" or
        password.strip() == "" or
        confirm_password.strip() == ""
    ):

        st.warning("Please fill all fields.")

    elif password != confirm_password:

        st.error("Passwords do not match.")

    elif len(password) < 6:

        st.error("Password must contain at least 6 characters.")

    else:

        try:

            create_user(
                full_name,
                email,
                hash_password(password)
            )

            st.success("🎉 Registration Successful!")

            st.info("You can now login.")

        except Exception:

            st.error("This email is already registered.")

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

st.divider()

st.info("Already have an account? Login from the Login page.")

show_footer()