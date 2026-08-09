import pandas as pd
from datetime import date
from pyxirr import xirr
from api import get_cash_transactions


# =====================================================
# CASH BALANCE
# =====================================================

def cash_balance():

    transactions = get_cash_transactions()

    if transactions is None or transactions.empty:

        return {
            "cash_balance": 0.0,
            "cash_added": 0.0,
            "cash_withdrawn": 0.0,
        }

    transactions["amount"] = pd.to_numeric(
        transactions["amount"],
        errors="coerce",
    ).fillna(0)

    transactions["running_balance"] = pd.to_numeric(
        transactions["running_balance"],
        errors="coerce",
    ).fillna(0)

    return {

        "cash_balance": float(
            transactions.iloc[0]["running_balance"]
        ),

        "cash_added": float(

            transactions.loc[
                transactions["transaction_type"].isin(
                    ["INITIAL", "DEPOSIT"]
                ),
                "amount",
            ].sum()

        ),

        "cash_withdrawn": float(

            transactions.loc[
                transactions["transaction_type"] == "WITHDRAW",
                "amount",
            ].sum()

        ),

    }


# =====================================================
# XIRR
# =====================================================

def calculate_xirr(current_portfolio_value):

    transactions = get_cash_transactions()

    if transactions is None or transactions.empty:
        return 0.0

    cashflows = []

    for _, row in transactions.iterrows():

        amount = pd.to_numeric(
            row["amount"],
            errors="coerce",
        )

        if pd.isna(amount):
            continue

        txn_type = row["transaction_type"]

        # Money invested
        if txn_type in ("INITIAL", "DEPOSIT"):
            amount = -amount

        # Money withdrawn
        elif txn_type == "WITHDRAW":
            amount = amount

        else:
            continue

        cashflows.append(
            (
                pd.to_datetime(
                    row["transaction_date"]
                ).date(),
                float(amount),
            )
        )

    # Current Portfolio Value

    cashflows.append(

        (
            date.today(),
            float(current_portfolio_value),
        )

    )

    if len(cashflows) < 2:
        return 0.0

    try:

        return round(
            xirr(cashflows) * 100,
            2,
        )

    except Exception as e:

        print("XIRR Error:", e)

        return 0.0


# =====================================================
# DASHBOARD SUMMARY
# =====================================================

def dashboard_summary(cash_df, calls_df):

    summary = {

        "total_holdings": 0,
        "open_calls": 0,
        "closed_calls": 0,
        "premium_collected": 0.0,
        "total_charges": 0.0,

    }

    # -------------------------------------------------
    # CASH HOLDINGS
    # -------------------------------------------------

    if cash_df is not None and not cash_df.empty:

        open_cash = cash_df.copy()

        if "status" in open_cash.columns:

            open_cash = open_cash[
                open_cash["status"] == "OPEN"
            ]

        summary["total_holdings"] = len(open_cash)

        if "charges" in open_cash.columns:

            summary["total_charges"] += (

                pd.to_numeric(

                    open_cash["charges"],
                    errors="coerce",

                )

                .fillna(0)

                .sum()

            )

    # -------------------------------------------------
    # COVERED CALLS
    # -------------------------------------------------

    if calls_df is not None and not calls_df.empty:

        calls = calls_df.copy()

        if "status" in calls.columns:

            open_df = calls[
                calls["status"] == "OPEN"
            ]

            closed_df = calls[
                calls["status"] == "CLOSED"
            ]

        else:

            open_df = calls
            closed_df = pd.DataFrame()

        summary["open_calls"] = len(open_df)

        summary["closed_calls"] = len(closed_df)

        # -----------------------------------------
        # Premium Collected
        # -----------------------------------------

        if {
            "sell_average",
            "quantity",
            "opening_charges",
        }.issubset(open_df.columns):

            premium = (

                pd.to_numeric(
                    open_df["sell_average"],
                    errors="coerce",
                )

                *

                pd.to_numeric(
                    open_df["quantity"],
                    errors="coerce",
                )

            )

            premium -= pd.to_numeric(
                open_df["opening_charges"],
                errors="coerce",
            ).fillna(0)

            summary["premium_collected"] = premium.sum()

        # -----------------------------------------
        # Charges
        # -----------------------------------------

        opening = 0

        closing = 0

        if "opening_charges" in calls.columns:

            opening = (

                pd.to_numeric(
                    calls["opening_charges"],
                    errors="coerce",
                )

                .fillna(0)

                .sum()

            )

        if "closing_charges" in calls.columns:

            closing = (

                pd.to_numeric(
                    calls["closing_charges"],
                    errors="coerce",
                )

                .fillna(0)

                .sum()

            )

        summary["total_charges"] += (

            opening + closing

        )

    return summary

# =====================================================
# PORTFOLIO SUMMARY
# =====================================================

def portfolio_summary(cash_df, call_df): 

    summary = { 

        "investment": 0.0, 
        "current_value": 0.0, 
        "equity_gain": 0.0, 
        "cash_charges": 0.0, 
        "option_profit": 0.0, 
        "option_charges": 0.0, 
        "premium_collected": 0.0, 
        "total_charges": 0.0, 
        "net_portfolio_pl": 0.0, 
        "cash_balance": 0.0, 
        "cash_added": 0.0, 
        "cash_withdrawn": 0.0, 
        "roi": 0.0, 
        "xirr": 0.0, 
    }

    # ================================================= 
    # # CASH HOLDINGS / EQUITY 
    # ================================================= 
    investment = 0.0 
    current_value = 0.0 
    equity_gain_before_charges = 0.0 
    cash_charges = 0.0 

    if cash_df is not None and not cash_df.empty: 
        cash = cash_df.copy() 

        numeric_columns = [ 
            "buy_average", "current_price", "quantity", "gain_loss", "realized_gain", "charges", 
        ] 

        for col in numeric_columns: 

            if col in cash.columns: 
                cash[col] = pd.to_numeric( 
                    cash[col], errors="coerce", 
                ).fillna(0) 

            else: 
                cash[col] = 0.0 

        # --------------------------------------------- 
        # Separate OPEN and CLOSED positions 
        # --------------------------------------------- 
        if "status" in cash.columns: 
            open_cash = cash[ 
                cash["status"].astype(str).str.upper() == "OPEN" 
            ] 

            closed_cash = cash[ 
                cash["status"].astype(str).str.upper() == "CLOSED" 
            ] 
        else: 
            open_cash = cash 
            closed_cash = pd.DataFrame( 
                columns=cash.columns 
            ) 

        # --------------------------------------------- # 
        # Investment 
        # --------------------------------------------- 
        
        if not open_cash.empty: 
            investment = ( 

                open_cash["buy_average"] 

                * 

                open_cash["quantity"]

            ).sum() 

        # ---------------------------------------------
        # Current Value 
        # --------------------------------------------- 
        
        if not open_cash.empty: 
            current_value = ( 

                open_cash["current_price"] 

                * 

                open_cash["quantity"] 

            ).sum() 

        # --------------------------------------------- 
        # Unrealized Gain 
        # --------------------------------------------- 
        
        unrealized_gain = 0.0 

        if not open_cash.empty: 
            unrealized_gain = ( 

                open_cash["gain_loss"] 
                .sum() 

            ) 

        # --------------------------------------------- 
        # Realized Gain 
        # --------------------------------------------- 
        
        realized_gain = 0.0 

        if ( 
            not closed_cash.empty 
            and "realized_gain" in closed_cash.columns 
        ): 
            realized_gain = ( 
                closed_cash["realized_gain"] 
                .sum() 
            ) 

        # --------------------------------------------- 
        # CASH POSITION CHARGES 
        # --------------------------------------------- 
         
        # Include charges from both OPEN and CLOSED 
        # cash positions because charges are real 
        # portfolio costs. 
        
        cash_charges = ( 

            cash["charges"] 

            .sum() 

        ) 

        # --------------------------------------------- 
        # EQUITY GAIN 
        # --------------------------------------------- 
         
        equity_gain_before_charges = ( 

            unrealized_gain 

            + 

            realized_gain 

        ) 

        equity_gain = ( 

            equity_gain_before_charges 

            - 

            cash_charges 

        ) 

        summary["investment"] = float( investment ) 

        summary["current_value"] = float( current_value ) 

        summary["cash_charges"] = float( cash_charges ) 

        summary["equity_gain"] = float( equity_gain ) 

    # ================================================= 
    # COVERED CALLS 
    # ================================================= 
    
    option_profit = 0.0 

    option_charges = 0.0 

    premium_collected = 0.0 

    if call_df is not None and not call_df.empty: 

        calls = call_df.copy() 

        numeric_columns = [ 
            "sell_average", "buy_average", "quantity", "opening_charges", "closing_charges", "net_profit", 
        ] 

        for col in numeric_columns: 

            if col in calls.columns: 

                calls[col] = pd.to_numeric( calls[col], errors="coerce", ).fillna(0) 

            else: calls[col] = 0.0 

        # --------------------------------------------- 
        # OPEN / CLOSED CALLS 
        # --------------------------------------------- 
        
        if "status" in calls.columns: 

            open_calls = calls[ calls["status"].astype(str).str.upper() == "OPEN" ] 

            closed_calls = calls[ calls["status"].astype(str).str.upper() == "CLOSED" ] 

        else: 

            open_calls = calls 

            closed_calls = pd.DataFrame( columns=calls.columns ) 

        # --------------------------------------------- 
        # OPEN PREMIUM COLLECTED 
        # --------------------------------------------- 
        
        if not open_calls.empty: 
            premium_collected = ( 
                open_calls["sell_average"] 

                * 

                open_calls["quantity"] 

                - 

                open_calls["opening_charges"] ).sum() 

        # --------------------------------------------- 
        # CLOSED OPTION PROFIT 
        # --------------------------------------------- 
         
        if ( not closed_calls.empty and "net_profit" in closed_calls.columns ): 
            option_profit = ( closed_calls["net_profit"] .sum() ) 

        # --------------------------------------------- 
        # OPTION CHARGES 
        # --------------------------------------------- 
        
        option_charges = ( calls["opening_charges"] .sum() + calls["closing_charges"] .sum() ) 

    # ================================================= 
    # STORE OPTION VALUES 
    # ================================================= 
     
    summary["option_profit"] = float( option_profit ) 
    summary["option_charges"] = float( option_charges ) 
    summary["premium_collected"] = float( premium_collected ) 

    # ================================================= 
    # TOTAL CHARGES 
    # ================================================= 
    
    summary["total_charges"] = ( 

        summary["cash_charges"] 

        + 

        summary["option_charges"] 
    ) 

    # ================================================= 
    # CASH BALANCE 
    # ================================================= 
    
    cash = cash_balance() 

    summary["cash_balance"] = cash[ "cash_balance" ] 

    summary["cash_added"] = cash[ "cash_added" ] 

    summary["cash_withdrawn"] = cash[ "cash_withdrawn" ] 

    # ================================================= 
    # NET PORTFOLIO P/L 
    # ================================================= 
    
    # Equity gain already includes cash-position # charges. # # Option profit is the net profit from CLOSED # covered calls. # # Premium collected represents income from OPEN # covered calls and is therefore added separately. 
    
    summary["net_portfolio_pl"] = ( 

        summary["equity_gain"] 

        + 

        summary["option_profit"] 

        + 

        summary["premium_collected"] 
    ) 

    # ================================================= 
    # CURRENT PORTFOLIO VALUE 
    # ================================================= 
    
    current_portfolio_value = ( summary["cash_balance"] + summary["current_value"] + summary["premium_collected"] ) 

    # ================================================= 
    # ROI 
    # ================================================= 
    
    if summary["cash_added"] != 0: 
        summary["roi"] = round( 
            ( 
                summary["net_portfolio_pl"] 

                / 

                summary["cash_added"] 

            ) 

            * 

            100, 

            2, 

            ) 

    else: summary["roi"] = 0.0 

    # ================================================= 
    # XIRR 
    # ================================================= 
    if summary["cash_added"] != 0:
        summary["xirr"] = calculate_xirr( current_portfolio_value )
    else:
        summary["xirr"] = 0.0
    return summary

# =====================================================
# CASH HOLDINGS SUMMARY
# =====================================================

def cash_holding_summary(cash_df):

    summary = {

        "total_holdings": 0,
        "investment": 0.0,
        "current_value": 0.0,
        "gain_loss": 0.0,

    }

    if cash_df is None or cash_df.empty:

        return summary

    cash = cash_df.copy()

    numeric_columns = [

        "buy_average",
        "current_price",
        "quantity",
        "gain_loss",
        "charges",

    ]

    for col in numeric_columns:

        if col in cash.columns:

            cash[col] = pd.to_numeric(

                cash[col],

                errors="coerce",

            ).fillna(0)

    if "status" in cash.columns:

        cash = cash[
            cash["status"] == "OPEN"
        ]

    summary["total_holdings"] = len(cash)

    summary["investment"] = (

        cash["buy_average"]

        *

        cash["quantity"]

    ).sum()

    summary["current_value"] = (

        cash["current_price"]

        *

        cash["quantity"]

    ).sum()

    summary["gain_loss"] = (

        cash["gain_loss"].sum()

        -

        cash["charges"].sum()

    )

    return summary