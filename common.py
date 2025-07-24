from openai import OpenAI
from PIL import Image
from pdf2image import convert_from_bytes
import base64
import re
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st




OpenAI.api_key = st.session_state.get("api_key")
client = OpenAI(api_key=OpenAI.api_key)
def pdf_to_images(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    return images


def encode_image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def extract_table(text):
    lines = [line for line in text.splitlines() if "|" in line and not line.startswith("|---")]
    table_text = "\n".join(lines)
    df = pd.read_csv(StringIO(table_text), sep="|", engine="python").dropna(axis=1, how="all")
    df.columns = df.columns.str.strip()
    df = df.astype(str).apply(lambda col: col.str.strip())
    return df    


def extract_value(label, text):
    print ("II")
    pattern = rf"\*\*{label}:\*\*\s*([-+]?[\d,]+\.\d+)"
    match = re.search(pattern, text)
    if match:
        # Remove commas and convert to float
        return float(match.group(1).replace(',', ''))
    return 1.0


def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def to_pdf(df):
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.6))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    buffer = BytesIO()
    plt.savefig(buffer, format='pdf', bbox_inches='tight')
    buffer.seek(0)
    return buffer.getvalue()


def get_instruments(text):
    table_lines = [line.strip() for line in text.split('\n') if line.strip().startswith('|')]
    cleaned_table = '\n'.join(table_lines)

    # Load using pandas
    from io import StringIO
    df = pd.read_csv(StringIO(cleaned_table), sep='|', engine='python', skipinitialspace=True)

    # Clean column headers and drop empty unnamed columns
    df.columns = [col.strip() for col in df.columns if col.strip() != '']
    df = df.dropna(how='all', axis=1)

    # Clean values (remove commas in numbers for numeric conversion if needed)

    # Display result
    instrument_list = df["Instrument"].tolist()
    print("Extracted Instruments:", instrument_list)
    print(df)