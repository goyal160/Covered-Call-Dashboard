import streamlit as st
from api import patch_covered_call, delete_covered_call

def render_actions(row):
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("✏ Edit", key=f"edit_{row['id']}"):
            st.session_state[f"edit_{row['id']}"]=True
    if st.session_state.get(f"edit_{row['id']}",False):
        with st.form(f"form_{row['id']}"):
            strike=st.number_input("Strike",value=float(row["strike"]))
            sell=st.number_input("Sell Average",value=float(row["sell_average"]))
            qty=st.number_input("Quantity",value=int(row["quantity"]))
            charges=st.number_input("Charges",value=float(row["charges"]))
            if st.form_submit_button("Save"):
                patch_covered_call(row["id"],{
                    "strike":strike,
                    "sell_average":sell,
                    "quantity":qty,
                    "charges":charges
                })
                st.success("Updated")
                st.rerun()
    with c2:
        if st.button("✔ Close", key=f"close_{row['id']}"):
            patch_covered_call(row["id"],{"status":"CLOSED"})
            st.success("Position Closed")
            st.rerun()
    with c3:
        if st.button("🗑 Delete", key=f"del_{row['id']}"):
            delete_covered_call(row["id"])
            st.success("Deleted")
            st.rerun()
