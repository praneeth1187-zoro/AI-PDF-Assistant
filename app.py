import streamlit as st
from PyPDF2 import PdfReader

st.title("📄 AI PDF Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:
    pdf = PdfReader(uploaded_file)

    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"Number of Pages: {len(pdf.pages)}")

    text = ""

    for page in pdf.pages:
        text += page.extract_text() or ""

    st.subheader("Extracted Text")
    st.text_area(
        "PDF Content",
        text,
        height=300
    )
