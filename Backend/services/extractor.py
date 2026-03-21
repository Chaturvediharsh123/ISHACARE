import pdfplumber
import pytesseract
from PIL import Image
import re

def extract_text(file_path):

    text = ""

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()
    else:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

    return text


def extract_values(text):

    patterns = {
        "hemoglobin": r"Hemoglobin\s*[:\-]?\s*(\d+\.?\d*)",
        "rbc": r"RBC\s*[:\-]?\s*(\d+\.?\d*)",
        "wbc": r"WBC\s*[:\-]?\s*(\d+\.?\d*)",
        "platelets": r"Platelets\s*[:\-]?\s*(\d+\.?\d*)",
        "glucose": r"Glucose\s*[:\-]?\s*(\d+\.?\d*)",
        "hba1c": r"HbA1c\s*[:\-]?\s*(\d+\.?\d*)",
        "cholesterol_total": r"Total Cholesterol\s*[:\-]?\s*(\d+\.?\d*)",
        "hdl": r"HDL\s*[:\-]?\s*(\d+\.?\d*)",
        "ldl": r"LDL\s*[:\-]?\s*(\d+\.?\d*)",
        "triglycerides": r"Triglycerides\s*[:\-]?\s*(\d+\.?\d*)",
        "urea": r"Urea\s*[:\-]?\s*(\d+\.?\d*)",
        "creatinine": r"Creatinine\s*[:\-]?\s*(\d+\.?\d*)",
        "bilirubin": r"Bilirubin\s*[:\-]?\s*(\d+\.?\d*)",
        "alt": r"ALT\s*[:\-]?\s*(\d+\.?\d*)",
        "ast": r"AST\s*[:\-]?\s*(\d+\.?\d*)"
    }

    data = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = float(match.group(1))

    return data