import streamlit as st

from api import login


def render_login():
    """
    Displays the login form.

    Returns
    -------
    bool
        True if user is already authenticated or login succeeds.
        False otherwise.
    """

    st.title("🔐 Covered Call Dashboard")

    with st.form("login_form"):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if submitted:

        if not username.strip():

            st.error("Please enter username.")

            return False

        if not password:

            st.error("Please enter password.")

            return False

        try:

            login(
                username=username,
                password=password,
            )

            st.success(
                "Login Successful"
            )

            st.rerun()

        except Exception:

            st.error(
                "Invalid username or password."
            )

    return False