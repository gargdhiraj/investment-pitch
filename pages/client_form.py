import streamlit as st
from InvestmentProfile import InvestmentProfile
from PIL import Image



if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please log in first.")
    st.stop()



st.set_page_config(page_title="Portfolio Analyzer", layout="centered")

# Set Streamlit page config with custom branding
# st.set_page_config(
#     page_title="BanyanBridge Consulting",
#     page_icon="🌳",
#     layout="centered"
# )

# # Custom CSS for theme styling
# st.markdown("""
#     <style>
#     body {
#         background-color: #FFFFFF;
#     }
#     .stApp {
#         background-color: #FFFFFF;
#         color: #FFFFFF;
#     }
#     h1, h2, h3, h4, h5, h6 {
#         color: #21482F !important;
#     }
#     .stButton>button {
#         background-color: #21482F;
#         color: #000000;
#         border-radius: 8px;
#         padding: 0.5em 1em;
#         border: none;
#     }
#     .stRadio > div {
#         background-color: #21482F;
#         border-radius: 10px;
#         padding: 10px;
#         margin-bottom: 10px;
#     }
#     </style>
# """, unsafe_allow_html=True)

st.image("https://banyanbridge.consulting/logo.png", width=200)  # Replace with real logo URL

st.title("Investor Readiness Questionnaire")

with st.form("investment_profile_form"):
    st.subheader("1. What is your primary investment goal?")
    goal = st.radio("", [
        "🟢 Long-term growth (5+ years)",
        "🟡 Medium-term income or preservation (2–5 years)",
        "🔴 Short-term gains or quick access to funds (less than 2 years)"
    ])

    st.subheader("2. How do you feel about risk and market fluctuations?")
    risk = st.radio("", [
        "🟢 Comfortable – I can tolerate ups and downs",
        "🟡 Cautious – I prefer balanced risk",
        "🔴 Uncomfortable – I want to avoid losing money"
    ])

    st.subheader("3. How much investing experience do you have?")
    experience = st.radio("", [
        "🟢 Experienced – I’ve invested in stocks, ETFs, or mutual funds",
        "🟡 Some – I’ve used a retirement account or robo-advisor",
        "🔴 None – I’m new to investing"
    ])

    st.subheader("4. Do you have an emergency fund (3–6 months of expenses)?")
    emergency_fund = st.checkbox("✅ Yes", value=False)

    st.subheader("5. What is your current debt situation?")
    debt = st.radio("", [
        "🟢 No high-interest debt (e.g. credit cards)",
        "🟡 Some manageable debt",
        "🔴 Significant high-interest debt"
    ])

    st.subheader("6. What is your income stability?")
    income = st.radio("", [
        "🟢 Stable – consistent income and job security",
        "🟡 Somewhat stable – minor uncertainty",
        "🔴 Unstable – irregular or unpredictable income"
    ])

    st.subheader("7. How soon might you need to access this investment?")
    access = st.radio("", [
        "🟢 Not for at least 5 years",
        "🟡 Within 3–5 years",
        "🔴 Within 1–2 years"
    ])

    submitted = st.form_submit_button("Submit")

if submitted:
    InvestmentProfile.goal = goal
    InvestmentProfile.risk_tolerance = risk
    InvestmentProfile.experience = experience
    InvestmentProfile.emergency_fund = emergency_fund
    InvestmentProfile.debt_status = debt
    InvestmentProfile.income_stability = income
    InvestmentProfile.access_need = access
    st.switch_page("pages/client_recommendation.py")


