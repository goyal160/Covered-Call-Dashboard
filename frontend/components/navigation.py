import streamlit as st

from config import ADMIN_URL


# =====================================================
# SECTION HEADER
# =====================================================

def section_header(
    title: str,
    page: str | None = None,
    label: str | None = None,
    icon: str | None = None,
):
    """
    Renders a section title with an optional action button.
    """

    if page:

        left, right = st.columns([8, 1])

        with left:
            st.subheader(title)

        with right:
            st.page_link(
                page,
                label=label,
                icon=icon,
            )

    else:

        st.subheader(title)


# =====================================================
# QUICK NAVIGATION
# =====================================================

def quick_navigation():

    st.subheader("⚡ Quick Navigation")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.page_link(
            "pages/Cash_Holdings.py",
            label="💰 Cash Holdings",
            icon="💰",
        )

    with c2:

        st.page_link(
            "pages/Covered_Calls.py",
            label="📞 Covered Calls",
            icon="📞",
        )

    with c3:

        st.markdown(
            f"[⚙ Django Admin]({ADMIN_URL})"
        )