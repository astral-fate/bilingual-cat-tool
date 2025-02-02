import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from docx import Document
import os
import io

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def preprocess_text(text):
    text = text.replace('-\n', '')
    text = text.replace('\n', ' ')
    abbreviations = ['Mr.', 'Mrs.', 'Dr.', 'Ms.', 'Jr.', 'Sr.', 'Prof.', 'St.']
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '[dot]'))
    return text


def create_dataframe_from_text(text):
    sentences = text.split('. ')
    sentences = [sentence.replace('[dot]', '.') for sentence in sentences]
    data = {'Sentence': sentences, 'Translation': [''] * len(sentences)}
    df = pd.DataFrame(data)
    return df


def save_to_word(df, output_path):
    doc = Document()
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Sentence'
    hdr_cells[1].text = 'Translation'

    for index, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = row['Sentence']
        row_cells[1].text = row['Translation']

    doc.save(output_path)


def main():
    st.title("PDF to Bilingual Word Converter")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        
        # Save the uploaded file to the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
          f.write(uploaded_file.read())

        # Process the file
        text = extract_text_from_pdf(file_path)
        processed_text = preprocess_text(text)
        df = create_dataframe_from_text(processed_text)
        output_filename = uploaded_file.name.rsplit('.', 1)[0] + '_processed.docx'
        output_path = os.path.join(PROCESSED_FOLDER, output_filename)
        save_to_word(df, output_path)

        # Download the file
        with open(output_path, 'rb') as f:
            file_data = f.read()
        
        st.download_button(
            label="Download Processed Word File",
            data=file_data,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        
        st.success("File processed and available for download!")

if __name__ == "__main__":
    main()
