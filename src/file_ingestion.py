import os
import fitz  
# import PyMuPDF
import pdfplumber

# from pdf2image import convert_from_path
# from PIL import Image
from docx import Document


def extract_text_from_pdf(pdf_path, ocr_enabled):
    """
    Extracts text from a PDF. Uses PyMuPDF for digital PDFs and OCR for scanned PDFs.
    
    Args:
        pdf_path (str): Path to the PDF file.
        ocr_enabled (bool): Whether to use OCR for scanned PDFs.

    Returns:
        str: Extracted text.
    """
    text = ""

    # Try extracting text using PyMuPDF (for digital PDFs)
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"PyMuPDF failed: {e}")

    # If no text found, try pdfplumber (alternative method)
    if not text.strip():
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        except Exception as e:
            print(f"pdfplumber failed: {e}")

    return text.strip()

def extract_text_from_docx(docx_path):
    """
    Extracts text from a DOCX file.

    Args:
        docx_path (str): Path to the DOCX file.

    Returns:
        str: Extracted text.
    """
    try:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return ""

def extract_text_from_txt(txt_path):
    """
    Extracts text from a TXT file.

    Args:
        txt_path (str): Path to the TXT file.

    Returns:
        str: Extracted text.
    """
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error processing TXT: {e}")
        return ""


# Example Usage
if __name__ == "__main__":
    file_path = "obinnaekesi-cv_ds_old.pdf"  # Change to an actual file path
    extracted_text = extract_text_from_pdf(file_path, ocr_enabled=True)
    
    print("\n--- Extracted Resume Text ---\n")
    print(extracted_text[:1000])  # Print first 1000 characters for preview
