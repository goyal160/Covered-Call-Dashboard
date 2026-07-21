import streamlit as st
import plotly.express as px


def render_cash_allocation(df):

    if df.empty:
        return

    chart = df.copy()

    chart["Investment"] = (
        chart["buy_average"] *
        chart["quantity"]
    )

    fig = px.pie(

        chart,

        names="script_name",

        values="Investment",

        hole=0.45,

        title="Portfolio Allocation",

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )