import streamlit as st

from api import delete_covered_call


# ============================================================
# DELETE OPEN POSITION
# ============================================================

def render_delete_position(row):
    """
    Delete confirmation for Open Covered Call.
    """

    if st.button(
        "🗑 Delete",
        key=f"delete_{row['id']}",
        use_container_width=True,
    ):
        st.session_state["delete_id"] = row["id"]

    if st.session_state.get("delete_id") != row["id"]:
        return

    st.warning(
        "Delete this Covered Call?"
    )

    yes, no = st.columns(2)

    with yes:

        if st.button(
            "YES",
            key=f"yes_{row['id']}",
            use_container_width=True,
        ):

            delete_covered_call(
                row["id"]
            )

            st.success(
                "Covered Call Deleted."
            )

            st.cache_data.clear()

            st.session_state["delete_id"] = None

            st.rerun()

    with no:

        if st.button(
            "Cancel",
            key=f"cancel_{row['id']}",
            use_container_width=True,
        ):

            st.session_state["delete_id"] = None

            st.rerun()


# ============================================================
# DELETE CLOSED POSITION
# ============================================================

def render_delete_closed_position(row):
    """
    Delete confirmation for Closed Covered Call.
    """

    if st.button(
        "🗑 Delete",
        key=f"delete_closed_{row['id']}",
        use_container_width=True,
    ):
        st.session_state["delete_closed_id"] = row["id"]

    if (
        st.session_state.get("delete_closed_id")
        != row["id"]
    ):
        return

    st.warning(
        "Delete this Closed Position?"
    )

    yes, no = st.columns(2)

    with yes:

        if st.button(
            "YES",
            key=f"yes_closed_{row['id']}",
            use_container_width=True,
        ):

            delete_covered_call(
                row["id"]
            )

            st.success(
                "Closed Position Deleted."
            )

            st.cache_data.clear()

            st.session_state["delete_closed_id"] = None

            st.rerun()

    with no:

        if st.button(
            "Cancel",
            key=f"cancel_closed_{row['id']}",
            use_container_width=True,
        ):

            st.session_state["delete_closed_id"] = None

            st.rerun()