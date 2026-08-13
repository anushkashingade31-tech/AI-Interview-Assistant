import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.title("🤖 AI Interview")

        # -----------------------------
        # User Info
        # -----------------------------

        if "user" in st.session_state:

            st.success(
                st.session_state["user"]["full_name"]
            )

        st.divider()

        # -----------------------------
        # Before Login
        # -----------------------------

        if "logged_in" not in st.session_state:

            st.page_link(
                "app.py",
                label="🏠 Home"
            )

            st.page_link(
                "pages/1_login.py",
                label="🔐 Login"
            )

            st.page_link(
                "pages/2_register.py",
                label="📝 Register"
            )

        # -----------------------------
        # After Login
        # -----------------------------

        else:

            st.page_link(
                "pages/3_dashboard.py",
                label="🏠 Dashboard"
            )

            st.page_link(
                "pages/4_resume.py",
                label="📄 Resume"
            )

            st.page_link(
                "pages/5_interview.py",
                label="🎤 Interview"
            )

            st.page_link(
                "pages/6_results.py",
                label="📊 Results"
            )

            st.page_link(
                "pages/7_history.py",
                label="📚 History"
            )

            st.divider()

            if st.button("🚪 Logout"):

                st.session_state.clear()

                st.switch_page("app.py")