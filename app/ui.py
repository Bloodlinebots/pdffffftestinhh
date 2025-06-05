import streamlit as st
from app.converter import images_to_pdf

def run_app():
    st.set_page_config(page_title="🖼️ Image to PDF Converter", layout="centered")
    st.title("🖼️📄 Image to PDF Converter")

    uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    pdf_name = st.text_input("Enter PDF filename", "converted")

    if uploaded_files:
        st.subheader("Preview:")
        for file in uploaded_files:
            st.image(file, width=300)

        if st.button("Convert to PDF"):
            pdf_file = images_to_pdf(uploaded_files)
            st.success("✅ PDF created successfully!")
            st.download_button("📥 Download PDF", data=pdf_file, file_name=f"{pdf_name}.pdf", mime="application/pdf")
    else:
        st.info("Please upload images to get started.")
