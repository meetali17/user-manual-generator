import fitz  # PyMuPDF
import docx
import markdown2

def extract_text_from_file(uploaded_file, file_type):
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)

    elif file_type == "docx":
        return extract_text_from_docx(uploaded_file)

    elif file_type == "md":
        return extract_text_from_md(uploaded_file)

    else:
        return "❌ Unsupported file type"

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_md(file):
    raw_md = file.read().decode("utf-8")
    html = markdown2.markdown(raw_md)
    return html  # Or convert HTML to plain text if needed
