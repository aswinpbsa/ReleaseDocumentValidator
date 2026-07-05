import os
import base64

from fastapi import Body

@app.post("/validate-document-json")
async def validate_document_json(document: dict = Body(...)):

    filename = document["name"]
    content = document["contentBytes"]

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