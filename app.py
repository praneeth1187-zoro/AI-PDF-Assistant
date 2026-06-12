import streamlit as st

st.title("AI PDF Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:
    st.success("PDF uploaded successfully!")