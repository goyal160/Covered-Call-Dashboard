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

        # =====================================================
        # USER
        # =====================================================

        st.success(
            f"Logged in as\n\n**{username}**"
        )

        st.divider()

        # =====================================================
        # DASHBOARD
        # =====================================================

        if show_dashboard:

            if st.button(
                "🏠 Dashboard",
                width="stretch",
            ):
                st.switch_page(
                    "Dashboard.py"
                )

        # =====================================================
        # DIVIDENDS
        # =====================================================

        st.subheader("💰 Dividends")

        if st.button(
            "📋 Dividend Management",
            width="stretch",
        ):
            st.switch_page(
                "pages/Dividends.py"
            )

        st.caption(
            "Add, view and delete dividend income"
        )

        st.divider()

        # =====================================================
        # LOGOUT
        # =====================================================

        if st.button(
            "🚪 Logout",
            width="stretch",
        ):
            logout()
            st.rerun()