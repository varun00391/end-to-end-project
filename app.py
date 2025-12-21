import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from tools.reader import extractor_agent

app = FastAPI(title="PDF Extractor API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health_check():
    return {"status": "PDF Extractor API is running"}


@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    #  Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Save uploaded file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        # Call your extractor agent
        extracted_text = extractor_agent(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 4Optional cleanup
        os.remove(file_path)

    # Return response
    return {
        "file_name": file.filename,
        "extracted_text": extracted_text
    }
