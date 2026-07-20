import pandas as pd
import requests

from config import API_URL

TIMEOUT = 15


# =====================================================
# Generic HTTP Helpers
# =====================================================

def _get(endpoint, params=None):
    response = requests.get(
        f"{API_URL}/{endpoint}/",
        params=params,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def _post(endpoint, data):
    response = requests.post(
        f"{API_URL}/{endpoint}/",
        json=data,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def _put(endpoint, pk, data):
    response = requests.put(
        f"{API_URL}/{endpoint}/{pk}/",
        json=data,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def _patch(endpoint, pk, data):
    response = requests.patch(
        f"{API_URL}/{endpoint}/{pk}/",
        json=data,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def _delete(endpoint, pk):
    response = requests.delete(
        f"{API_URL}/{endpoint}/{pk}/",
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return True


# =====================================================
# DataFrame Helper
# =====================================================

def get_dataframe(endpoint, numeric_columns=None, params=None):

    data = _get(endpoint, params=params)

    df = pd.DataFrame(data)

    if df.empty:
        return df

    if numeric_columns:
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce",
                )

    return df


# =====================================================
# CASH HOLDINGS
# =====================================================

def get_cash_holdings():

    return get_dataframe(
        "cash-holdings",
        [
            "buy_average",
            "current_price",
            "quantity",
            "investment",
            "current_value",
            "gain_loss",
            "charges",
        ],
    )


def get_cash_holding(pk):
    return _get(f"cash-holdings/{pk}")


def create_cash_holding(data):
    return _post("cash-holdings", data)


def update_cash_holding(pk, data):
    return _put("cash-holdings", pk, data)


def patch_cash_holding(pk, data):
    return _patch("cash-holdings", pk, data)


def delete_cash_holding(pk):
    return _delete("cash-holdings", pk)


# =====================================================
# COVERED CALLS
# =====================================================

def get_covered_calls():

    return get_dataframe(
        "covered-calls",
        [
            "strike",
            "sell_average",
            "buy_average",
            "quantity",
            "charges",
            "net_profit",
        ],
    )


def get_open_calls():

    return get_dataframe(
        "covered-calls",
        [
            "strike",
            "sell_average",
            "buy_average",
            "quantity",
            "charges",
            "net_profit",
        ],
        params={
            "status": "OPEN",
        },
    )


def get_closed_calls():

    return get_dataframe(
        "covered-calls",
        [
            "strike",
            "sell_average",
            "buy_average",
            "quantity",
            "charges",
            "net_profit",
        ],
        params={
            "status": "CLOSED",
        },
    )


def get_covered_call(pk):
    return _get(f"covered-calls/{pk}")


def create_covered_call(data):
    return _post("covered-calls", data)


def update_covered_call(pk, data):
    return _put("covered-calls", pk, data)


def patch_covered_call(pk, data):
    return _patch("covered-calls", pk, data)


def delete_covered_call(pk):
    return _delete("covered-calls", pk)