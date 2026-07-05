import os
import shutil
import base64

from fastapi import FastAPI, UploadFile, File, Body

from validators.filename_validator import validate_filename
from engine.document_extractor import DocumentExtractor
from engine.content_validator import ContentValidator

app = FastAPI(
    title="Release Governance Validation API",
    version="1.0.0"
)

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

extractor = DocumentExtractor()
validator = ContentValidator()


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Release Governance Validation API is running!"
    }


# -----------------------------
# Existing Swagger Upload API
# -----------------------------
@app.post("/validate-document")
async def validate_document(file: UploadFile = File(...)):

    upload_path = os.path.join("uploads", file.filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    filename_result = validate_filename(file.filename)

    extracted = extractor.extract(upload_path)

    validation_result = validator.validate(
        extracted,
        filename_result["documentType"]
    )

    return {
        "filename": file.filename,
        "filenameValidation": filename_result,
        "validation": validation_result
    }


# ----------------------------------------------------
# Copilot Studio + Power Automate Endpoint
# Body = document dynamic token
# ----------------------------------------------------
@app.post("/validate-document-json")
async def validate_document_json(document: dict = Body(...)):

    try:
        filename = document.get("name")
        content = document.get("contentBytes")

        if not filename:
            return {
                "status": "FAIL",
                "message": "Filename missing."
            }

        if not content:
            return {
                "status": "FAIL",
                "message": "Document content missing."
            }

        upload_path = os.path.join("uploads", filename)

        with open(upload_path, "wb") as f:
            f.write(base64.b64decode(content))

        filename_result = validate_filename(filename)

        extracted = extractor.extract(upload_path)

        validation_result = validator.validate(
            extracted,
            filename_result["documentType"]
        )

        return {
            "filename": filename,
            "filenameValidation": filename_result,
            "validation": validation_result
        }

    except Exception as ex:
        return {
            "status": "ERROR",
            "message": str(ex)
        }