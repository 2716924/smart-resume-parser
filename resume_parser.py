# resume_parser.py

import fitz  # PyMuPDF
import sys

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resume_parser.py <resume.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    extracted = extract_text_from_pdf(pdf_path)
    print("\nExtracted Text:\n", extracted[:1000])  # Print first 1000 characters
