from docx import Document


def read_document(file_path):

    document = Document(file_path)

    paragraphs = []

    for para in document.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text.strip())

    return paragraphs