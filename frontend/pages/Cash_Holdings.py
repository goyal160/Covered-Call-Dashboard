
import streamlit as st
import plotly.express as px
from api import (
    get_cash_holdings,
    create_cash_holding,
    patch_cash_holding,
    delete_cash_holding,
)
from services import cash_holding_summary

st.set_page_config(page_title="Cash Holdings", layout="wide")
st.title("💰 Cash Holdings")

cash = get_cash_holdings()
summary = cash_holding_summary(cash)

c1,c2,c3,c4=st.columns(4)
c1.metric("Holdings", summary["total_holdings"])
c2.metric("Investment", f"₹ {summary['investment']:,.2f}")
c3.metric("Current Value", f"₹ {summary['current_value']:,.2f}")
c4.metric("Gain/Loss", f"₹ {summary['gain_loss']:,.2f}")

st.divider()

col1,col2=st.columns([3,2])
search=col1.text_input("🔍 Search Script")
sort_by=col2.selectbox("Sort By",["Script","Investment","Gain/Loss"])

if not cash.empty:
    if search:
        cash=cash[cash["script_name"].str.contains(search,case=False,na=False)]

    cash["Investment"]=cash["buy_average"]*cash["quantity"]

    if sort_by=="Script":
        cash=cash.sort_values("script_name")
    elif sort_by=="Investment":
        cash=cash.sort_values("Investment",ascending=False)
    else:
        cash=cash.sort_values("gain_loss",ascending=False)

with st.expander("➕ Add Holding"):
    with st.form("cash_form"):
        a,b,c=st.columns(3)
        script=a.text_input("Script Name")
        buy=b.number_input("Buy Average",0.0,format="%.2f")
        current=c.number_input("Current Price",0.0,format="%.2f")
        d,e=st.columns(2)
        qty=d.number_input("Quantity",1,step=1)
        charges=e.number_input("Charges",0.0,format="%.2f")
        if st.form_submit_button("Add Holding"):
            create_cash_holding({
                "script_name":script,
                "buy_average":buy,
                "current_price":current,
                "quantity":qty,
                "charges":charges
            })
            st.success("Holding Added Successfully")
            st.rerun()

# =====================================================
# CURRENT HOLDINGS
# =====================================================

st.subheader("Current Holdings")

if cash.empty:

    st.info("No holdings available.")

else:

    # ---------------------------------------------
    # Prepare Display Data
    # ---------------------------------------------

    cash["Current Value"] = (

        cash["current_price"]

        *

        cash["quantity"]

    )

    display = cash[

        [

            "script_name",

            "buy_average",

            "current_price",

            "quantity",

            "Investment",

            "Current Value",

            "gain_loss",

            "charges",

        ]

    ].copy()

    display.columns = [

        "Script",

        "Buy Avg",

        "Current Price",

        "Qty",

        "Investment",

        "Current Value",

        "Gain/Loss",

        "Charges",

    ]

    # =====================================================
    # HOLDING CARDS
    # =====================================================

    for _, row in cash.iterrows():

        title = (
            f"📈 {row['script_name']}  |  "
            f"Qty : {int(row['quantity'])}"
        )

        with st.expander(title):

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    f"**Buy Average :** ₹ {row['buy_average']:,.2f}"
                )

                st.write(
                    f"**Current Price :** ₹ {row['current_price']:,.2f}"
                )

                st.write(
                    f"**Quantity :** {int(row['quantity'])}"
                )

                st.write(
                    f"**Investment :** ₹ {row['Investment']:,.2f}"
                )

            with c2:

                current_value = (
                    row["current_price"]
                    *
                    row["quantity"]
                )

                st.write(
                    f"**Current Value :** ₹ {current_value:,.2f}"
                )

                st.write(
                    f"**Gain/Loss :** ₹ {row['gain_loss']:,.2f}"
                )

                st.write(
                    f"**Charges :** ₹ {row['charges']:,.2f}"
                )

            st.divider()

            edit_col, delete_col = st.columns(2)

            # ==========================================
            # EDIT
            # ==========================================

            with edit_col:

                if st.button(
                    "✏ Edit",
                    key=f"edit_{row['id']}"
                ):

                    st.session_state[
                        "edit_cash"
                    ] = row["id"]

            if st.session_state.get(
                "edit_cash"
            ) == row["id"]:

                with st.form(
                    f"edit_cash_{row['id']}"
                ):

                    buy = st.number_input(
                        "Buy Average",
                        value=float(row["buy_average"]),
                        format="%.2f",
                    )

                    current = st.number_input(
                        "Current Price",
                        value=float(row["current_price"]),
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

                    if st.form_submit_button(
                        "Save Changes"
                    ):

                        patch_cash_holding(

                            row["id"],

                            {

                                "buy_average": buy,

                                "current_price": current,

                                "quantity": qty,

                                "charges": charges,

                            },

                        )

                        st.success(
                            "Holding Updated Successfully."
                        )

                        st.rerun()

        # ==========================================
        # DELETE
        # ==========================================

        with delete_col:

            if st.button(
                "🗑 Delete",
                key=f"delete_{row['id']}"
            ):

                st.session_state[
                    "delete_cash"
                ] = row["id"]

        if st.session_state.get(
            "delete_cash"
        ) == row["id"]:

            st.warning(
                "Delete this holding?"
            )

            yes, no = st.columns(2)

            with yes:

                if st.button(
                    "YES",
                    key=f"yes_{row['id']}"
                ):

                    delete_cash_holding(
                        row["id"]
                    )

                    st.success(
                        "Holding Deleted."
                    )

                    st.rerun()

            with no:

                if st.button(
                    "Cancel",
                    key=f"cancel_{row['id']}"
                ):

                    st.session_state[
                        "delete_cash"
                    ] = None

                    st.rerun()

    # ---------------------------------------------
    # Portfolio Allocation
    # ---------------------------------------------

    fig = px.pie(

        cash,

        names="script_name",

        values="Investment",

        hole=0.45,

        title="Portfolio Allocation",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

    st.divider()

    # ---------------------------------------------
    # EXPORT
    # ---------------------------------------------

    csv = display.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        "📄 Download CSV",

        csv,

        "cash_holdings.csv",

        "text/csv",

        use_container_width=True,

    )

    try:

        from io import BytesIO

        output = BytesIO()

        with pd.ExcelWriter(

            output,

            engine="openpyxl",

        ) as writer:

            display.to_excel(

                writer,

                index=False,

            )

        st.download_button(

            "📊 Download Excel",

            output.getvalue(),

            "cash_holdings.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True,

        )

    except Exception:

        st.warning(

            "openpyxl not installed. Excel export unavailable."

        )

st.divider()