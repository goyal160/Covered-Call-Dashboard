import pandas as pd


# =====================================================
# DASHBOARD SUMMARY
# =====================================================

def dashboard_summary(cash_df, calls_df):
    """
    Dashboard KPIs not included in portfolio_summary().
    """

    summary = {
        "total_holdings": 0,
        "open_calls": 0,
        "closed_calls": 0,
        "premium_collected": 0.0,
        "total_charges": 0.0,
    }

    if cash_df is not None and not cash_df.empty:

        summary["total_holdings"] = len(cash_df)

        if "charges" in cash_df.columns:

            summary["total_charges"] += (
                cash_df["charges"]
                .fillna(0)
                .sum()
            )

    if calls_df is not None and not calls_df.empty:

        if "status" in calls_df.columns:

            open_df = calls_df[
                calls_df["status"] == "OPEN"
            ]

            closed_df = calls_df[
                calls_df["status"] == "CLOSED"
            ]

            summary["open_calls"] = len(open_df)

            summary["closed_calls"] = len(closed_df)

            if (
                "sell_average" in open_df.columns
                and
                "quantity" in open_df.columns
            ):

                summary["premium_collected"] = (

                    open_df["sell_average"]

                    *

                    open_df["quantity"]

                ).sum()

        if "charges" in calls_df.columns:

            summary["total_charges"] += (

                calls_df["charges"]

                .fillna(0)

                .sum()

            )

    return summary


# =====================================================
# PORTFOLIO SUMMARY
# =====================================================

def portfolio_summary(cash_df, call_df):

    summary = {}

    investment = 0
    current_value = 0
    equity_gain = 0
    cash_charges = 0

    if cash_df is not None and not cash_df.empty:

        investment = (

            cash_df["buy_average"]

            *

            cash_df["quantity"]

        ).sum()

        current_value = (

            cash_df["current_price"]

            *

            cash_df["quantity"]

        ).sum()

        equity_gain = (

            cash_df["gain_loss"]

            .fillna(0)

            .sum()

            -

            cash_df["charges"]

            .fillna(0)

            .sum()

        )

        cash_charges = (

            cash_df["charges"]

            .fillna(0)

            .sum()

        )

    summary["investment"] = investment
    summary["current_value"] = current_value
    summary["equity_gain"] = equity_gain
    summary["cash_charges"] = cash_charges

    option_profit = 0
    option_charges = 0

    if call_df is not None and not call_df.empty:

        if "net_profit" in call_df.columns:

            option_profit = (

                call_df["net_profit"]

                .fillna(0)

                .sum()

            )

        elif {

            "sell_average",

            "buy_average",

            "quantity",

        }.issubset(call_df.columns):

            closed = call_df.copy()

            if "status" in closed.columns:

                closed = closed[
                    closed["status"] == "CLOSED"
                ]

            option_profit = (

                (

                    closed["sell_average"]

                    -

                    closed["buy_average"]

                )

                *

                closed["quantity"]

            ).sum()

        if "charges" in call_df.columns:

            option_charges = (

                call_df["charges"]

                .fillna(0)

                .sum()

            )

    summary["option_profit"] = option_profit
    summary["option_charges"] = option_charges

    premium_collected = 0

    if not call_df.empty:

        required = {
            "status",
            "sell_average",
            "quantity",
        }

        if required.issubset(call_df.columns):

            premium_collected = (

                call_df.loc[
                    call_df["status"] == "OPEN",
                    "sell_average",
                ]

                *

                call_df.loc[
                    call_df["status"] == "OPEN",
                    "quantity",
                ]

            ).sum()

    summary["premium_collected"] = premium_collected

    summary["charges"] = option_charges

    summary["net_portfolio_pl"] = (

        equity_gain

        +

        option_profit

        +

        premium_collected

    )

    summary["roi"] = (

        round(

            summary["net_portfolio_pl"]

            /

            investment

            *

            100,

            2,

        )

        if investment

        else 0

    )

    return summary


# =====================================================
# CASH HOLDINGS SUMMARY
# =====================================================

def cash_holding_summary(cash_df):

    summary = {

        "total_holdings": 0,

        "investment": 0,

        "current_value": 0,

        "gain_loss": 0,

    }

    if cash_df is None or cash_df.empty:

        return summary

    summary["total_holdings"] = len(cash_df)

    summary["investment"] = (

        cash_df["buy_average"]

        *

        cash_df["quantity"]

    ).sum()

    summary["current_value"] = (

        cash_df["current_price"]

        *

        cash_df["quantity"]

    ).sum()

    summary["gain_loss"] = (

        cash_df["gain_loss"]

        .fillna(0)

        .sum()

        -

        cash_df["charges"]

        .fillna(0)

        .sum()

    )

    return summary