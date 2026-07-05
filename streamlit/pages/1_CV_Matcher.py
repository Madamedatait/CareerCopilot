import streamlit as st

st.title("📄 CV Matcher")

uploaded_file = st.file_uploader(
    "Upload your CV",
    type=["pdf"]
)

if uploaded_file:
    st.success("CV uploaded")