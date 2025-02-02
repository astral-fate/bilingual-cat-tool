

# Bilingual CAT Tool (PDF to Editable Word)

This project provides a free and open-source alternative to commercial Computer-Assisted Translation (CAT) tools for extracting text from PDF documents and preparing them for bilingual translation. It aims to streamline the translation process by segmenting text into sentences and presenting them in a table format suitable for translators to input translations.

## Motivation

### The Need for Accessible CAT Tools
Commercial CAT tools offer many advanced features that are valuable for professional translators. However, the cost of these tools can be prohibitive for many individuals, small teams, or community translators working on personal or non-profit projects.

This project was born out of the necessity to have a simple, accessible, and free tool that provides the core functionality of a CAT tool. This includes:

- **Text Extraction:** Accurately extracting text from PDFs.
- **Segmentation:** Breaking down the extracted text into manageable segments, typically sentences.
- **Editable Format:** Presenting these segments in an easily editable format (such as a Word document) where translations can be directly added.

### Addressing the Paywall
Many individuals require CAT functionalities, but the paywalls of current products make this impossible. By creating an open source solution, we aim to provide users with full access to their work. This democratizes translation tools for researchers, non-profits and general use.

### Project Scope and Limitations
It is important to note that this project **does not** aim to replace professional CAT tools in terms of advanced features. We do not offer translation memory, terminology management, machine translation integration, or other advanced functionality.

Our goal is to create a basic but usable tool that makes the initial stages of translation (text extraction, segmentation, preparation) more accessible and manageable.

## How It Works

The project operates through a Streamlit web application that takes a PDF as input and generates a processed Word document with the text prepared for bilingual translation. Here is the breakdown of the core steps:

1. **PDF Upload:** The user uploads a PDF document via a file upload widget.
2. **Text Extraction:** The tool uses the `PyMuPDF` library to extract the text content from the uploaded PDF.
3. **Preprocessing:** The extracted text goes through a series of preprocessing steps:
   - Replacing line breaks that were created to simulate soft-breaks in PDFs ( `-\n`)
   - Replacing all newlines (`\n`) with spaces.
   - Replacing any abbreviations such as 'Mr.', 'Mrs.' with `[dot]` so that sentences can be split correctly in the next step.
4. **Segmentation:** The preprocessed text is split into individual sentences, using the period followed by a space (`. `) as the delimiter. These sentences represent the "segments." Any instances of abbreviations that were modified in the last step are changed back to their original format by changing `[dot]` to `.`
5. **Dataframe Creation:** The segments (sentences) are organized into a Pandas DataFrame with two columns:
   - **Sentence:** This column contains the original text segment (sentence).
   - **Translation:** This column is initially empty. It is designed for translators to enter the corresponding translated text.
6. **Word Document Creation:** The DataFrame is then converted into an editable Word document format (using `python-docx`). The document is created with a two column table. The first column is the extracted segments and the second column is for translators to enter their translations.
7. **Download:** Finally, the generated Word document is provided as a download link to the user.

## Usage

# The deployed app can be used [here](https://bilingual-cat-tool.streamlit.app/)

![image](https://github.com/user-attachments/assets/260cf2eb-4192-4162-a304-b2ca4e4e2ca8)
