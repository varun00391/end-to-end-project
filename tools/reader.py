import fitz  # or import pymupdf as fitz

def extractor_agent(pdf_path):
    doc = fitz.open(pdf_path)  # open the document
    text = ""
    for page in doc:
        text += page.get_text() # extract text from each page
    doc.close()
    return text



