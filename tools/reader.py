import fitz  # or import pymupdf as fitz

def extractor_agent(pdf_path):
    doc = fitz.open(pdf_path)  # open the document
    text = ""
    for page in doc:
        text += page.get_text() # extract text from each page
    doc.close()
    return text


# import re
# import fitz  # PyMuPDF


# def extract_text_and_tables(pdf_path: str) -> dict:
#     doc = fitz.open(pdf_path)

#     result = {
#         "file": pdf_path,
#         "pages": []
#     }

#     for page_num, page in enumerate(doc, start=1):
#         page_dict = page.get_text("dict")

#         text_blocks = []
#         table_blocks = []

#         for block in page_dict["blocks"]:
#             # Text block
#             if block["type"] == 0:
#                 block_text = ""

#                 for line in block["lines"]:
#                     for span in line["spans"]:
#                         block_text += span["text"] + " "

#                 block_text = block_text.strip()

#                 if not block_text:
#                     continue

#                 # Heuristic: detect table-like text
#                 if is_table_like(block_text):
#                     table_blocks.append(block_text)
#                 else:
#                     text_blocks.append(block_text)

#         result["pages"].append({
#             "page_number": page_num,
#             "text_blocks": text_blocks,
#             "tables": table_blocks
#         })

#     doc.close()
#     return result


# def is_table_like(text: str) -> bool:
#     lines = text.split("\n")

#     if len(lines) < 2:
#         return False

#     numeric_ratio = sum(
#         any(char.isdigit() for char in line) for line in lines
#     ) / len(lines)

#     # if most lines contain numbers → likely a table
#     return numeric_ratio > 0.6



