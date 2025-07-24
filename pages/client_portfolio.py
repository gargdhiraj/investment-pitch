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
from common import pdf_to_images, encode_image_to_base64, extract_table, client, extract_value
from InvestmentProfile import InvestmentProfile
from prompts import analyze_current_portfolio_prompt

def analyze_portfolio(uploaded_file):
    all_text = ""
    all_images = []
    if "excel" in uploaded_file.type:
        df = pd.read_excel(uploaded_file)
        st.subheader("📊 Uploaded Portfolio")
        st.dataframe(df)
        all_text = df.to_string()
    elif "pdf" in uploaded_file.type:
        pdf_images = pdf_to_images(uploaded_file.read())
        all_images = pdf_images[:1]  # Use first page
    elif "image" in uploaded_file.type:
        image = Image.open(uploaded_file)
        all_images = [image]
        

    return all_text, all_images


def get_ai_response(uploaded_file):
    with st.spinner("🔍 Analyzing your portfolio..."):

        if uploaded_file is None:
            st.error("Please upload a file first.")
            return ""
        all_text, all_images = analyze_portfolio(uploaded_file)
        if all_images:
            base64_img = encode_image_to_base64(all_images[0])
            vision_prompt = analyze_current_portfolio_prompt
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": vision_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]}
                ],
                max_tokens=2000
            )
            ai_output = response.choices[0].message.content
            # ai_output =f"""
            # ### Portfolio Table

            #     | Stock Name | Quantity | Average Price | Invested    | LTP    | LTP %   | P&L        | P&L %  |
            #     |------------|----------|---------------|-------------|--------|---------|------------|--------|
            #     | DEVYANI    | 839      | 178.58        | 1,49,829.36 | 173.00 | 3.50%   | -4,682.36  | -3.13% |
            #     | GAIL       | 0 / 517  | 193.39        | 99,984.15   | 193.41 | 0.35%   | +8.82      | 0.01%  |
            #     | GOLD1      | 1491     | 80.43         | 1,19,935.16 | 81.45  | -0.13%  | +1,506.79  | 1.26%  |
            #     | TATAMOTORS | 980      | 727.07        | 7,12,534.40 | 689.05 | -0.20%  | -37,265.40 | -5.23% |

            #     ### Portfolio Summary

            #     - **Total Invested:** 10,82,283.07
            #     - **Current Value:** 10,41,850.92
            #     - **P&L:** -40,432.15
            #     - **Day's P&L:** +3,767.53 (+0.36%)
            # """
            # print("AI Output:", ai_output)


            # Example usage
            InvestmentProfile.current_value = extract_value("Current", ai_output)
            print("Extracted Current Value:", InvestmentProfile.current_value )
            InvestmentProfile.total_invested = extract_value("Total Invested", ai_output)
            InvestmentProfile.AI_output = ai_output
            # --- DISPLAY ---

            st.markdown(ai_output)


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please log in first.")
    st.stop()




uploaded_file = InvestmentProfile.uploaded_file


st.set_page_config(page_title="Portfolio Analyzer", layout="centered")
st.title("📤 Your Current Portfolio")
if st.button("Next"):
    print(InvestmentProfile.AI_output)
    if InvestmentProfile.AI_output == "" or InvestmentProfile.AI_output is None:
        st.error("Your portfolio is not analyzed yet. Please upload a file first.")
    else:
        st.switch_page("pages/client_form.py")
get_ai_response(uploaded_file)