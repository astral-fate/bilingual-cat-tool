from flask import Flask, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import pandas as pd
from docx import Document
import os

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file
            text = extract_text_from_pdf(file_path)
            processed_text = preprocess_text(text)
            df = create_dataframe_from_text(processed_text)
            output_filename = filename.rsplit('.', 1)[0] + '_processed.docx'
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            save_to_word(df, output_path)
            
            return redirect(url_for('download_file', filename=output_filename))
    
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
