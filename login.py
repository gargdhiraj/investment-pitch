import streamlit as st



st.set_page_config(page_title="Login", layout="centered")

# --- HARDCODED LOGIN DETAILS ---
USERNAME = "admin"
PASSWORD = "admin"  # Store in environment variables in real apps!

st.title("🔐 Portfolio Analyzer Login")

# --- LOGIN FORM ---
with st.form("login_form"):
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    api = st.text_input("API Key", type="password", help="Enter your API key if required.")

    # user ="admin"
    # pw = "admin"  # Hardcoded for demo purposes, replace with input fields in real apps

    submit = st.form_submit_button("Login")

    if submit:
        if user == USERNAME and pw == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.session_state.api_key = api
            st.switch_page("pages/client_upload.py")
        else:
            st.error("Invalid credentials. Please try again.")
