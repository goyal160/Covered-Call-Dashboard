import streamlit as st
import pandas as pd
from datetime import date

from api import (
    get_open_calls,
    get_closed_calls,
    get_cash_holdings,
    create_covered_call,
    patch_covered_call,
    delete_covered_call,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Covered Calls",
    page_icon="📞",
    layout="wide",
)

st.title("📞 Covered Calls")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=5)
def load_data():
    open_df = get_open_calls()
    closed_df = get_closed_calls()
    holdings_df = get_cash_holdings()

    return open_df, closed_df, holdings_df


open_df, closed_df, holdings = load_data()


# ============================================================
# ENSURE DATAFRAMES
# ============================================================

if open_df is None:
    open_df = pd.DataFrame()

if closed_df is None:
    closed_df = pd.DataFrame()

if holdings is None:
    holdings = pd.DataFrame()


# ============================================================
# CALCULATE KPI VALUES
# ============================================================

open_calls = len(open_df)

closed_calls = len(closed_df)

premium_collected = 0

if not open_df.empty:

    premium_collected = (
        open_df["sell_average"] *
        open_df["quantity"]
    ).sum()


realized_profit = 0

if (
    not closed_df.empty and
    "net_profit" in closed_df.columns
):

    realized_profit = closed_df["net_profit"].sum()


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Open Calls",
    open_calls
)

k2.metric(
    "Closed Calls",
    closed_calls
)

k3.metric(
    "Premium Collected",
    f"₹ {premium_collected:,.2f}"
)

k4.metric(
    "Realized Profit",
    f"₹ {realized_profit:,.2f}"
)


st.divider()


# ============================================================
# ADD COVERED CALL
# ============================================================

with st.expander(
    "➕ Sell New Covered Call",
    expanded=False
):

    if holdings.empty:

        st.warning(
            "Please create a Cash Holding first."
        )

    else:

        with st.form(
            "new_covered_call"
        ):

            holding_name = st.selectbox(
                "Holding",
                holdings["script_name"].tolist()
            )

            col1, col2 = st.columns(2)

            with col1:

                trade_date = st.date_input(
                    "Trade Date",
                    value=date.today()
                )

                expiry_date = st.date_input(
                    "Expiry Date"
                )

                strike = st.number_input(
                    "Strike",
                    min_value=0.0,
                    format="%.2f"
                )

            with col2:

                sell_average = st.number_input(
                    "Sell Average",
                    min_value=0.0,
                    format="%.2f"
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    step=1
                )

                charges = st.number_input(
                    "Charges",
                    min_value=0.0,
                    format="%.2f"
                )

            submitted = st.form_submit_button(
                "Save Covered Call",
                width="stretch"
            )

            if submitted:

                holding_id = int(

                    holdings.loc[
                        holdings["script_name"]
                        == holding_name,
                        "id",
                    ].iloc[0]

                )

                create_covered_call(

                    {

                        "holding": holding_id,

                        "trade_date": str(
                            trade_date
                        ),

                        "expiry_date": str(
                            expiry_date
                        ),

                        "strike": strike,

                        "sell_average": sell_average,

                        "buy_average": 0,

                        "quantity": quantity,

                        "charges": charges,

                        "status": "OPEN",

                    }

                )

                st.success(
                    "Covered Call Added Successfully."
                )

                st.cache_data.clear()

                st.rerun()


# ============================================================
# SEARCH + SORT
# ============================================================

left, right = st.columns([3, 1])

with left:

    search = st.text_input(
        "🔍 Search Holding",
        ""
    )

with right:

    sort_by = st.selectbox(

        "Sort By",

        [

            "Trade Date",

            "Expiry",

            "Strike",

            "Premium",

            "Quantity",

        ]

    )


# ============================================================
# FILTER OPEN POSITIONS
# ============================================================

display_open = open_df.copy()

if (
    not display_open.empty
    and search.strip()
):

    if "holding_name" in display_open.columns:

        display_open = display_open[
            display_open[
                "holding_name"
            ].str.contains(
                search,
                case=False,
                na=False,
            )
        ]


if not display_open.empty:

    if sort_by == "Strike":

        display_open = display_open.sort_values(
            "strike"
        )

    elif sort_by == "Quantity":

        display_open = display_open.sort_values(
            "quantity",
            ascending=False
        )

    elif sort_by == "Premium":

        display_open = display_open.sort_values(
            "sell_average",
            ascending=False
        )

    elif sort_by == "Trade Date":

        display_open = display_open.sort_values(
            "trade_date"
        )

    elif sort_by == "Expiry":

        display_open = display_open.sort_values(
            "expiry_date"
        )

# ============================
# PART 2 STARTS HERE
# ============================

# ============================================================
# TABS
# ============================================================

tab_open, tab_closed = st.tabs(
    [
        "🟢 Open Positions",
        "🔴 Closed Positions",
    ]
)

# ============================================================
# OPEN POSITIONS
# ============================================================

with tab_open:

    if display_open.empty:

        st.info(
            "No Open Covered Call Positions."
        )

    else:

        st.subheader(
            "Open Covered Calls"
        )

        for _, row in display_open.iterrows():

            holding = row.get(
                "holding_name",
                "Holding"
            )

            premium = (
                float(row["sell_average"])
                *
                int(row["quantity"])
            )

            title = (
                f"📌 {holding}"
                f" | Strike {row['strike']}"
                f" | Qty {row['quantity']}"
            )

            with st.expander(
                title,
                expanded=False
            ):

                c1, c2 = st.columns(2)

                with c1:

                    st.write(
                        "**Trade Date**"
                    )
                    st.write(
                        row["trade_date"]
                    )

                    st.write(
                        "**Expiry Date**"
                    )
                    st.write(
                        row["expiry_date"]
                    )

                    st.write(
                        "**Strike**"
                    )
                    st.write(
                        row["strike"]
                    )

                    st.write(
                        "**Sell Average**"
                    )
                    st.write(
                        row["sell_average"]
                    )

                with c2:

                    st.write(
                        "**Quantity**"
                    )
                    st.write(
                        row["quantity"]
                    )

                    st.write(
                        "**Charges**"
                    )
                    st.write(
                        row["charges"]
                    )

                    st.write(
                        "**Premium Collected**"
                    )
                    st.write(
                        f"₹ {premium:,.2f}"
                    )

                    st.write(
                        "**Status**"
                    )
                    st.success("OPEN")

                st.divider()

                col1, col2, col3 = st.columns(3)

                # ====================================================
                # EDIT
                # ====================================================

                with col1:

                    if st.button(
                        "✏ Edit",
                        key=f"edit_{row['id']}"
                    ):

                        st.session_state[
                            "edit_id"
                        ] = row["id"]

                if (
                    st.session_state.get(
                        "edit_id"
                    )
                    == row["id"]
                ):

                    with st.form(
                        f"edit_form_{row['id']}"
                    ):

                        strike = st.number_input(
                            "Strike",
                            value=float(
                                row["strike"]
                            ),
                            format="%.2f",
                        )

                        sell = st.number_input(
                            "Sell Average",
                            value=float(
                                row["sell_average"]
                            ),
                            format="%.2f",
                        )

                        qty = st.number_input(
                            "Quantity",
                            value=int(
                                row["quantity"]
                            ),
                        )

                        charges = st.number_input(
                            "Charges",
                            value=float(
                                row["charges"]
                            ),
                            format="%.2f",
                        )

                        if st.form_submit_button(
                            "Save Changes"
                        ):

                            patch_covered_call(

                                row["id"],

                                {

                                    "strike": strike,

                                    "sell_average": sell,

                                    "quantity": qty,

                                    "charges": charges,

                                },

                            )

                            st.success(
                                "Position Updated."
                            )

                            st.cache_data.clear()

                            st.rerun()

                # ====================================================
                # CLOSE POSITION
                # ====================================================

                with col2:

                    if st.button(
                        "✔ Close Position",
                        key=f"close_{row['id']}"
                    ):

                        st.session_state[
                            "close_id"
                        ] = row["id"]

                if (
                    st.session_state.get(
                        "close_id"
                    )
                    == row["id"]
                ):

                    with st.form(
                        f"close_form_{row['id']}"
                    ):

                        buy_avg = st.number_input(
                            "Buy Average",
                            min_value=0.0,
                            format="%.2f",
                        )

                        close_date = st.date_input(
                            "Close Date"
                        )

                        close_charge = st.number_input(
                            "Closing Charges",
                            min_value=0.0,
                            format="%.2f",
                        )

                        if st.form_submit_button(
                            "Close Position"
                        ):

                            patch_covered_call(

                                row["id"],

                                {

                                    "buy_average": buy_avg,

                                    "charges": close_charge,

                                    "close_date": str(
                                        close_date
                                    ),

                                    "status": "CLOSED",

                                },

                            )

                            st.success(
                                "Position Closed."
                            )

                            st.cache_data.clear()

                            st.rerun()

                # ====================================================
                # DELETE
                # ====================================================

                with col3:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{row['id']}"
                    ):

                        st.session_state[
                            "delete_id"
                        ] = row["id"]

                if (
                    st.session_state.get(
                        "delete_id"
                    )
                    == row["id"]
                ):

                    st.warning(
                        "Delete this Covered Call?"
                    )

                    yes, no = st.columns(2)

                    with yes:

                        if st.button(
                            "YES",
                            key=f"yes_{row['id']}"
                        ):

                            delete_covered_call(
                                row["id"]
                            )

                            st.success(
                                "Deleted Successfully."
                            )

                            st.cache_data.clear()

                            st.rerun()

                    with no:

                        if st.button(
                            "Cancel",
                            key=f"cancel_{row['id']}"
                        ):

                            st.session_state[
                                "delete_id"
                            ] = None

                            st.rerun()

# ============================================================
# CLOSED POSITIONS
# ============================================================

with tab_closed:

    if closed_df.empty:

        st.info("No Closed Positions.")

    else:

        st.subheader("Closed Covered Calls")

        for _, row in closed_df.iterrows():

            holding = row.get(
                "holding_name",
                row.get("script_name", "Holding")
            )

            title = (
                f"✅ {holding}"
                f" | Strike {row['strike']}"
                f" | Qty {row['quantity']}"
            )

            with st.expander(title, expanded=False):

                c1, c2 = st.columns(2)

                with c1:

                    st.write("**Trade Date**")
                    st.write(row["trade_date"])

                    st.write("**Expiry Date**")
                    st.write(row["expiry_date"])

                    st.write("**Strike**")
                    st.write(row["strike"])

                    st.write("**Sell Average**")
                    st.write(row["sell_average"])

                    st.write("**Buy Average**")
                    st.write(row["buy_average"])

                with c2:

                    st.write("**Quantity**")
                    st.write(row["quantity"])

                    st.write("**Charges**")
                    st.write(row["charges"])

                    st.write("**Close Date**")
                    st.write(row["close_date"])

                    if "net_profit" in row.index:
                        st.write("**Net Profit**")
                        st.success(
                            f"₹ {row['net_profit']:,.2f}"
                        )

                    st.write("**Status**")
                    st.success("CLOSED")

                st.divider()

                col1, col2 = st.columns(2)

                # ====================================================
                # EDIT CLOSED POSITION
                # ====================================================

                with col1:

                    if st.button(
                        "✏ Edit",
                        key=f"edit_closed_{row['id']}"
                    ):

                        st.session_state[
                            "edit_closed_id"
                        ] = row["id"]

                if (
                    st.session_state.get(
                        "edit_closed_id"
                    ) == row["id"]
                ):

                    with st.form(
                        f"edit_closed_form_{row['id']}"
                    ):

                        strike = st.number_input(
                            "Strike",
                            value=float(row["strike"]),
                            format="%.2f",
                        )

                        sell_avg = st.number_input(
                            "Sell Average",
                            value=float(row["sell_average"]),
                            format="%.2f",
                        )

                        buy_avg = st.number_input(
                            "Buy Average",
                            value=float(row["buy_average"]),
                            format="%.2f",
                        )

                        qty = st.number_input(
                            "Quantity",
                            value=int(row["quantity"]),
                            min_value=1,
                        )

                        charges = st.number_input(
                            "Charges",
                            value=float(row["charges"]),
                            format="%.2f",
                        )

                        close_date = st.date_input(
                            "Close Date",
                            value=pd.to_datetime(
                                row["close_date"]
                            ).date(),
                        )

                        if st.form_submit_button(
                            "Save Changes"
                        ):

                            patch_covered_call(

                                row["id"],

                                {

                                    "strike": strike,

                                    "sell_average": sell_avg,

                                    "buy_average": buy_avg,

                                    "quantity": qty,

                                    "charges": charges,

                                    "close_date": str(close_date),

                                },

                            )

                            st.success(
                                "Closed Position Updated."
                            )

                            st.cache_data.clear()

                            st.rerun()

                # ====================================================
                # DELETE
                # ====================================================

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_closed_{row['id']}"
                    ):

                        st.session_state[
                            "delete_closed_id"
                        ] = row["id"]

                if (
                    st.session_state.get(
                        "delete_closed_id"
                    ) == row["id"]
                ):

                    st.warning(
                        "Delete this Closed Position?"
                    )

                    yes, no = st.columns(2)

                    with yes:

                        if st.button(
                            "YES",
                            key=f"yes_closed_{row['id']}"
                        ):

                            delete_covered_call(
                                row["id"]
                            )

                            st.success(
                                "Position Deleted."
                            )

                            st.cache_data.clear()

                            st.rerun()

                    with no:

                        if st.button(
                            "Cancel",
                            key=f"cancel_closed_{row['id']}"
                        ):

                            st.session_state[
                                "delete_closed_id"
                            ] = None

                            st.rerun()