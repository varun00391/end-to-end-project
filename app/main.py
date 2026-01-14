import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.tools.reader import extractor_agent

import time
from fastapi import Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST


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
app = FastAPI(title="New PDF Extractor API")


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------
# Prometheus Metrics
# ------------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)

# ========================
# 🆕 METRICS MIDDLEWARE
# ========================
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(duration)

    return response

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

# ========================
# 🆕 METRICS ENDPOINT
# ========================
@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )