import pandas as pd


# =====================================================
# DATAFRAME HELPERS
# =====================================================

def ensure_dataframe(df):
    """
    Returns an empty DataFrame if df is None.
    """
    return df if isinstance(df, pd.DataFrame) else pd.DataFrame()


# =====================================================
# SAFE NUMERIC
# =====================================================

def safe_sum(df, column):
    """
    Safely returns sum of a numeric column.
    """

    if (
        df.empty
        or column not in df.columns
    ):
        return 0.0

    return (
        pd.to_numeric(
            df[column],
            errors="coerce",
        )
        .fillna(0)
        .sum()
    )


def safe_count(df):
    return 0 if df.empty else len(df)


def safe_filter(df, column, value):
    """
    Safe filtering.
    """

    if (
        df.empty
        or column not in df.columns
    ):
        return pd.DataFrame()

    return df[df[column] == value]


# =====================================================
# FORMATTERS
# =====================================================

def money(value):

    try:

        return f"₹ {float(value):,.2f}"

    except Exception:

        return "₹ 0.00"


def percent(value):

    try:

        return f"{float(value):,.2f}%"

    except Exception:

        return "0.00%"


# =====================================================
# DATE HELPERS
# =====================================================

def format_date(value):

    if pd.isna(value):
        return ""

    value = pd.to_datetime(
        value,
        errors="coerce",
    )

    if pd.isna(value):
        return ""

    return value.strftime("%d-%b-%Y")


# =====================================================
# DATAFRAME CONVERSION
# =====================================================

NUMERIC_COLUMNS = [

    "buy_average",
    "sell_average",
    "current_price",
    "strike",
    "charges",
    "investment",
    "current_value",
    "gain_loss",
    "net_profit",
    "quantity",

]

DATE_COLUMNS = [

    "trade_date",
    "expiry_date",
    "close_date",

]


def clean_dataframe(df):

    if df.empty:
        return df

    for column in NUMERIC_COLUMNS:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            ).fillna(0)

    for column in DATE_COLUMNS:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    return df