import streamlit as st
import plotly.express as px


# =====================================================
# PORTFOLIO ALLOCATION PIE CHART
# =====================================================

def portfolio_allocation_chart(cash_df):
    """
    Displays portfolio allocation pie chart.
    """

    st.subheader("📊 Portfolio Allocation")

    if cash_df.empty:

        st.info(
            "No Cash Holdings Available."
        )

        return

    allocation = cash_df.copy()

    allocation["Holding Value"] = (

        allocation["current_price"]

        *

        allocation["quantity"]

    )

    # Support either column name
    name_column = (
        "holding_name"
        if "holding_name" in allocation.columns
        else "script_name"
    )

    fig = px.pie(

        allocation,

        names=name_column,

        values="Holding Value",

        hole=0.45,

        title="Portfolio Allocation",

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label",

    )

    fig.update_layout(

        legend_title="",

        margin=dict(
            t=60,
            b=20,
            l=20,
            r=20,
        ),

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        },
    )


# =====================================================
# HOLDING DISTRIBUTION BAR CHART
# (Optional future use)
# =====================================================

def holding_value_chart(cash_df):
    """
    Horizontal bar chart of holding values.
    """

    if cash_df.empty:
        return

    data = cash_df.copy()

    data["Holding Value"] = (

        data["current_price"]

        *

        data["quantity"]

    )

    name_column = (
        "holding_name"
        if "holding_name" in data.columns
        else "script_name"
    )

    fig = px.bar(

        data,

        x="Holding Value",

        y=name_column,

        orientation="h",

        text="Holding Value",

        title="Holding Value by Script",

    )

    fig.update_layout(

        height=480,

        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10,
        ),

        legend=dict(
            orientation="h",
            y=-0.12,
            x=0.5,
            xanchor="center",
        ),

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )