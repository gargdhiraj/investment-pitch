import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
from openai import OpenAI
from PIL import Image
from pdf2image import convert_from_bytes
import base64
import re
import fitz  # PyMuPDF
from PIL import Image
from InvestmentProfile import InvestmentProfile
from common import pdf_to_images, encode_image_to_base64, extract_table, client, extract_value, to_excel, to_pdf, get_instruments
from prompts import recommendation_new_portfolio_prompt


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please log in first.")
    st.stop()


def get_ai_recommendation():
    with st.spinner("🔍 Analyzing your portfolio for recmomendation..."):
        vision_prompt = recommendation_new_portfolio_prompt + f"""
            
            Cliet investment prefernes are: 
            goal = {InvestmentProfile.goal},
            risk_tolerance = {InvestmentProfile.risk_tolerance}, 
            experience = {InvestmentProfile.experience},
            emergency_fund = {InvestmentProfile.emergency_fund},
            debt_status = {InvestmentProfile.debt_status},
            income_stability = {InvestmentProfile.income_stability},
            access_need = {InvestmentProfile.access_need}    
            Client current investment profile is: {InvestmentProfile.AI_output}
            
        """

        if InvestmentProfile.more_recommendation==True:
            vision_prompt += f"""
            Dont inlcude stocks from : {InvestmentProfile.previous_recommended_portfolio}
            """
            InvestmentProfile.more_recommendation = False
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(vision_prompt)
        print(InvestmentProfile.previous_recommended_portfolio)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": vision_prompt},
                ]}
            ],
            max_tokens=2000
        )
        ai_output = response.choices[0].message.content

        # ai_output = """
        #     Revised Portfolio Strategy
        #     Considering the client's investment preferences...

        #     | Instrument           | Ticker     | Sector        | Investment Amount (INR) | Reason                                                                             |
        #     |----------------------|------------|---------------|-------------------------|------------------------------------------------------------------------------------|
        #     | TCS                  | TCS        | Technology    | 2,00,000                | Strong growth potential in the tech sector and a global presence.                  |
        #     | HDFCBANK             | HDFCBANK   | Financial     | 2,00,000                | Leading bank in India with stable growth prospects and good management.            |
        #     | SBI Gold ETF         | SBIGETFDB  | Commodities   | 1,00,000                | Provides exposure to gold, acting as a hedge against inflation and market downturns.|
        #     | NIPORT100            | NIPORT100  | Index ETF     | 1,00,000                | Diversifies risk by tracking the top 100 stocks, offering market-wide exposure.     |
        #     | SBI Nifty Next 50    | NNF50MF    | Mutual Fund   | 1,82,283                | Access to a diversified set of mid-cap companies with growth potential.             |
        #     | India Govt Bond      | -          | Bonds         | 2,00,000                | Ensures stability and provides a fixed income stream to balance equity risk.       |
        #     | Reliance Industries  | RELIANCE   | Conglomerate  | 1,00,000                | Diversified operations with strong growth prospects and good dividend history.     |

        #     Portfolio Allocation Explanation...        
        # """
        

        stocks = get_instruments(ai_output)
        InvestmentProfile.latest_recommendation_portfolio = ai_output
        if InvestmentProfile.previous_recommended_portfolio is None:
            InvestmentProfile.previous_recommended_portfolio = stocks
        else:
            InvestmentProfile.previous_recommended_portfolio += "\n" + stocks
            

        # elif all_text:
        #     text_prompt = f"""
        #     The following is a portfolio:\n{all_text}\n
        #     The user's investment goal is: {final_goal}.
        #     Suggest a revised {currency_symbol}{investment_amount if investment_amount != 'auto' else '[CURRENT VALUE]'} portfolio in {currency}.
        #     """
        #     response = client.chat.completions.create(
        #         model="gpt-4o",
        #         messages=[{"role": "user", "content": text_prompt}]
        #     )
        #     ai_output = response.choices[0].message.content

    # --- DISPLAY ---
    st.subheader("Portfolio Suggestions")
    st.markdown(InvestmentProfile.latest_recommendation_portfolio)
    print (InvestmentProfile.latest_recommendation_portfolio)
    InvestmentProfile.more_recommendation=True

def __init__():
    get_ai_recommendation()
    st.set_page_config(page_title="Analyze Portfolio", layout="centered")
    st.title("📈Portfolio Analysis")

if st.button("🔄 Get More Recommendations", key="more_recommendation"):
    InvestmentProfile.more_recommendation = True
    get_ai_recommendation()
# --- PARSE SUGGESTED TABLE ---
# try:
#     df_suggestion = extract_table(InvestmentProfile.latest_recommendation_portfolio)
#     st.subheader("📋 Suggested Portfolio Table")
#     st.dataframe(df_suggestion)

#     st.download_button("📥 Download Excel", to_excel(df_suggestion), file_name="Suggested_Portfolio.xlsx")
#     st.download_button("📥 Download PDF", to_pdf(df_suggestion), file_name="Suggested_Portfolio.pdf")
# except Exception as e:
#     st.warning("⚠️ Could not auto-parse the table. Please copy manually.")
#     st.code(str(e))



