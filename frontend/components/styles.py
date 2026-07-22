import streamlit as st

def load_css():

    st.markdown("""
    <style>

    # div[data-testid="stMetric"]{
    #     padding:0.3rem 0.4rem;
    # }

    # div[data-testid="stMetric"] > label{
    #     font-size:0.78rem;
    # }

    # div[data-testid="stMetricValue"]{
    #     font-size:1.15rem;
    # }

    </style>
    """, unsafe_allow_html=True)