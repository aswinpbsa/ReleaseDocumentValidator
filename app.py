import os
import shutil

from fastapi import FastAPI, UploadFile, File

from validators.filename_validator import validate_filename
from engine.document_extractor import DocumentExtractor
from engine.content_validator import ContentValidator

app = FastAPI(
    title="Release Governance Validation API",
    version="1.0.0"
)

extractor = DocumentExtractor()
validator = ContentValidator()


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Release Governance Validation API is running!"
    }


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