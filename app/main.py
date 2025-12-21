import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.tools.reader import extractor_agent

# ------------------------
# Logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("pdf-api")

# ------------------------
# App
# ------------------------
app = FastAPI(title="PDF Extractor API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    logger.info(f"Received file upload: {file.filename}")

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        logger.info(f"File saved temporarily: {file_path}")

        # Extract
        extracted_text = extractor_agent(file_path)

        logger.info(f"Extraction successful: {file.filename}")

        return {
            "file_name": file.filename,
            "extracted_text": extracted_text
        }

    except Exception as e:
        logger.exception("PDF extraction failed")
        raise HTTPException(status_code=500, detail="PDF processing failed")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file removed: {file_path}")

