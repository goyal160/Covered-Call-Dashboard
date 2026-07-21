import streamlit as st

from api import logout


def render_sidebar(
    username: str,
    show_dashboard: bool = False,
):
    """
    Common sidebar for all pages.

    Parameters
    ----------
    username : str
        Logged in username.

    show_dashboard : bool
        If True, show Dashboard button.
        Used by pages inside /pages.
    """

    with st.sidebar:

        st.success(
            f"Logged in as\n\n**{username}**"
        )

        st.divider()

        if show_dashboard:

            if st.button(
                "🏠 Dashboard",
                use_container_width=True,
            ):

                st.switch_page(
                    "Dashboard.py"
                )

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):

            logout()
            st.rerun()