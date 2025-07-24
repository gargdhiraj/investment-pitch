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



if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please log in first.")
    st.stop()


st.set_page_config(page_title="Portfolio Analyzer", layout="centered")
st.title("📤 Upload Portfolio Document")

uploaded_file = st.file_uploader("📎 Upload your Portfolio File (Image, PDF, Excel)", type=["jpg", "jpeg", "png", "pdf", "xlsx", "xls"])

# with open("sample_portfolio.jpeg", "rb") as f:  # Replace with your local image path
#     uploaded_file = BytesIO(f.read()) 
#     image = Image.open(uploaded_file)
#     st.image(image, caption="📊 Simulated Uploaded Image", use_column_width=True)


if uploaded_file is not None:
    InvestmentProfile.uploaded_file = uploaded_file
    InvestmentProfile.file_uploaded = True  
    col1, col2 = st.columns([3, 1])  # Adjust width ratio as needed

    with col1:
        st.markdown("Your Portfolio")


    with col2:
        if st.button("Next"):
            st.session_state.uploaded_file = uploaded_file
            st.session_state.file_uploaded = True
            st.switch_page("pages/client_portfolio.py")

    print(uploaded_file)
    file_type = uploaded_file.type
    if "excel" in file_type:
        df = pd.read_excel(uploaded_file)
        st.subheader("📊 Uploaded Portfolio")
        st.dataframe(df)
    elif "pdf" in file_type:
        pdf_images = pdf_to_images(uploaded_file.read())
        st.image(pdf_images[0], caption="PDF Page 1", use_container_width=True)
    elif "image" in file_type:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)



# --- SESSION STATE ---
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False



elif not uploaded_file:
    st.warning("Please upload a document before continuing.")

