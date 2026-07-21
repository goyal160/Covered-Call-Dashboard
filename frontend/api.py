import requests
import pandas as pd
import streamlit as st
from utils import clean_dataframe
from config import API_URL

# ==========================================================
# SESSION
# ==========================================================

session = requests.Session()


# ==========================================================
# AUTH HEADER
# ==========================================================

def auth_header():

    token = st.session_state.get("token")

    if token:
        return {
            "Authorization": f"Token {token}"
        }

    return {}


# ==========================================================
# GENERIC REQUEST
# ==========================================================

def request(
    method,
    endpoint,
    payload=None,
    params=None,
):

    response = session.request(

        method=method,

        url=f"{API_URL}/{endpoint}",

        json=payload,

        params=params,

        headers=auth_header(),

        timeout=20,

    )

    response.raise_for_status()

    if response.content:

        return response.json()

    return None


# ==========================================================
# LOGIN
# ==========================================================

def login(username, password):

    response = session.post(

        f"{API_URL}/auth/login/",

        json={
            "username": username,
            "password": password,
        },

        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    st.session_state["token"] = data["token"]
    st.session_state["username"] = data["username"]

    return data


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    token = st.session_state.get("token")

    if token:

        try:

            session.post(

                f"{API_URL}/auth/logout/",

                headers=auth_header(),

                timeout=20,

            )

        except Exception:
            pass

    clear_session()


# ==========================================================
# DATAFRAME HELPER
# ==========================================================

def get_dataframe(endpoint, params=None):

    data = request(
        "GET",
        endpoint,
        params=params,
    )

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    return clean_dataframe(df)

# ==========================================================
# CASH HOLDINGS
# ==========================================================

def get_cash_holdings():
    return get_dataframe("cash-holdings/")


def get_cash_holding(pk):
    return request("GET", f"cash-holdings/{pk}/")


def create_cash_holding(data):
    return request("POST", "cash-holdings/", payload=data)


def patch_cash_holding(pk, data):
    return request("PATCH", f"cash-holdings/{pk}/", payload=data)


def delete_cash_holding(pk):
    request("DELETE", f"cash-holdings/{pk}/")
    return True


# ==========================================================
# COVERED CALLS
# ==========================================================

def get_covered_calls():
    return get_dataframe("covered-calls/")


def get_open_calls():
    return get_dataframe(
        "covered-calls/",
        params={"status": "OPEN"},
    )


def get_closed_calls():
    return get_dataframe(
        "covered-calls/",
        params={"status": "CLOSED"},
    )


def get_covered_call(pk):
    return request("GET", f"covered-calls/{pk}/")


def create_covered_call(data):
    return request(
        "POST",
        "covered-calls/",
        payload=data,
    )


def patch_covered_call(pk, data):
    return request(
        "PATCH",
        f"covered-calls/{pk}/",
        payload=data,
    )


def update_covered_call(pk, data):
    return patch_covered_call(pk, data)


def close_covered_call(
    pk,
    buy_average,
    close_date,
    charges,
):

    payload = {

        "buy_average": buy_average,

        "close_date": str(close_date),

        "charges": charges,

        "status": "CLOSED",

    }

    return patch_covered_call(pk, payload)


def reopen_covered_call(pk):

    payload = {

        "status": "OPEN",

        "buy_average": 0,

        "close_date": None,

    }

    return patch_covered_call(pk, payload)


def delete_covered_call(pk):
    request("DELETE", f"covered-calls/{pk}/")
    return True


# ==========================================================
# AUTH HELPERS
# ==========================================================

def is_logged_in():
    return "token" in st.session_state


def get_logged_in_user():
    return st.session_state.get(
        "username",
        "",
    )


def clear_session():

    st.session_state.pop(
        "token",
        None,
    )

    st.session_state.pop(
        "username",
        None,
    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

def api_available():

    try:

        response = session.get(
            API_URL,
            timeout=5,
        )

        return response.status_code < 500

    except Exception:

        return False