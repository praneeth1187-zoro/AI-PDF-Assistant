import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


# Extract text from PDF
def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# Split text into chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)
    return chunks


# Create and save FAISS vector store
def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(
        text_chunks,
        embedding=embeddings
    )

    vector_store.save_local("faiss_index")


# Streamlit UI
def main():
    st.set_page_config(page_title="AI PDF Assistant")

    st.title("📄 AI PDF Assistant")

    pdf = st.file_uploader(
        "Upload a PDF file",
        type="pdf"
    )

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        num_pages = len(pdf_reader.pages)

        st.success(f"PDF Uploaded Successfully!")
        st.write(f"Number of Pages: {num_pages}")

        # Reset pointer and extract text
        pdf.seek(0)
        text = get_pdf_text(pdf)

        st.subheader("Extracted Text Preview")
        st.text_area(
            "Text",
            text[:2000],
            height=300
        )

        if st.button("Process PDF"):
            with st.spinner("Creating FAISS Index..."):
                chunks = get_text_chunks(text)
                get_vector_store(chunks)

            st.success("FAISS Index Created Successfully!")
            st.write("Saved in: ./faiss_index")


if __name__ == "__main__":
    main()
