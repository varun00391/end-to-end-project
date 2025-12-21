from tools.reader import extractor_agent

pdf_file = "MultiPage_Report.pdf"

data = extractor_agent(pdf_file)
print(data)









# from tools.reader import extract_text_and_tables


# pdf_file = "MultiPage_Report.pdf"

# # data = extract_text_and_tables(pdf_file)
# data = extract_text_and_tables(pdf_file)

# for page in data["pages"]:
#     print(f"\n--- Page {page['page_number']} ---")
#     print("TEXT:")
#     for t in page["text_blocks"]:
#         print("-", t[:100])

#     print("\nTABLES:")
#     for tbl in page["tables"]:
#         print("-", tbl[:100])




