import instructor
from models import Invoice
import pymupdf
import requests
import os

from api_key import GEMINI_API_KEY

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

client = instructor.from_provider("gemini/gemini-3.5-flash-lite")

def repackaging(pdf):
    # If it's a URL, download it first
    if pdf.startswith("http://") or pdf.startswith("https://"):
        r = requests.get(pdf)
        pdf_path = "temp_downloaded.pdf"
        with open(pdf_path, "wb") as f:
            f.write(r.content)
    else:
        pdf_path = pdf

    doc = pymupdf.open(pdf_path)

    text = ""
    tables_data = []
    for page in doc:
        text += page.get_text()
        found = page.find_tables()
        for t in found:
            tables_data.append(t.extract())

    generator = client.chat.completions.create(
        response_model=Invoice,
        messages=[
            {
                "role": "user",
                "content": f"Extract invoice from this text and tables.\nTEXT:\n{text}\nTABLES:\n{tables_data}",
            }
        ],
    )

    return generator