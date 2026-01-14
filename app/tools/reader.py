import fitz  # or import pymupdf as fitz
import logging

logger = logging.getLogger("pdf-api.reader")

# def extractor_agent(pdf_path):
#     doc = fitz.open(pdf_path)  # open the document
#     text = ""
#     for page in doc:
#         text += page.get_text() # extract text from each page
#     doc.close()
#     return text

import fitz  # PyMuPDF
import logging

logger = logging.getLogger("pdf-api.reader")


def extractor_agent(pdf_path: str) -> str:
    logger.info(f"Starting PDF extraction: {pdf_path}")

    text = ""
    try:
        doc = fitz.open(pdf_path)

        for page_number, page in enumerate(doc, start=1):
            page_text = page.get_text()
            text += page_text

            logger.debug(f"Extracted page {page_number}")

        doc.close()

        logger.info(f"Completed PDF extraction: {pdf_path}")

    except Exception as e:
        logger.exception(f"Failed to extract PDF: {pdf_path}")
        raise

    return text




