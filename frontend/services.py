import pandas as pd


def portfolio_summary(cash_df, call_df):

    summary = {}

    # =====================================================
    # CASH HOLDINGS
    # =====================================================

    if cash_df.empty:

        investment = 0
        current_value = 0
        equity_gain = 0
        cash_charges = 0

    else:

        investment = (
            cash_df["buy_average"] *
            cash_df["quantity"]
        ).sum()

        current_value = (
            cash_df["current_price"] *
            cash_df["quantity"]
        ).sum()

        equity_gain = (
            cash_df["gain_loss"]
        ).sum()

        cash_charges = (
            cash_df["charges"]
        ).sum()

    summary["investment"] = investment
    summary["current_value"] = current_value
    summary["equity_gain"] = equity_gain
    summary["cash_charges"] = cash_charges

    # =====================================================
    # COVERED CALLS
    # =====================================================

    option_profit = 0
    option_charges = 0

    if not call_df.empty:

        if "option_profit" in call_df.columns:

            option_profit = (
                call_df["option_profit"]
            ).fillna(0).sum()

        elif (
            "sell_average" in call_df.columns
            and
            "buy_average" in call_df.columns
            and
            "quantity" in call_df.columns
        ):

            closed = call_df.copy()

            if "status" in closed.columns:

                closed = closed[
                    closed["status"] == "CLOSED"
                ]

            if not closed.empty:

                option_profit = (

                    (
                        closed["sell_average"]
                        -
                        closed["buy_average"].fillna(0)
                    )

                    *

                    closed["quantity"]

                ).sum()

        if "charges" in call_df.columns:

            option_charges = (
                call_df["charges"]
            ).fillna(0).sum()

    summary["option_profit"] = option_profit
    summary["option_charges"] = option_charges

    # =====================================================
    # TOTALS
    # =====================================================

    summary["charges"] = (
        cash_charges +
        option_charges
    )

    summary["overall_pl"] = (

        equity_gain

        +

        option_profit

        -

        summary["charges"]

    )

    if investment == 0:

        summary["roi"] = 0

    else:

        summary["roi"] = round(

            (

                summary["overall_pl"]

                /

                investment

            )

            *

            100,

            2,

        )

    return summary


def cash_holding_summary(cash_df):

    summary = {

        "total_holdings": 0,

        "investment": 0,

        "current_value": 0,

        "gain_loss": 0,

    }

    if cash_df.empty:

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

    ).sum()

    return summary