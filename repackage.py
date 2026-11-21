from google import genai
import instructor
from models import Invoice
import pymupdf

client = instructor.from_provider("gemini/gemini-3.5-flash-lite")

def repackaging(pdf):
    doc = pymupdf.open(pdf)
    text = ""
    for page in doc:
        text += page.get_text()

    tables = []
    for page in doc:
        tables = page.find_tables()
        for line in tables:
            tables.append(line)

    generator = client.chat.completions.create(
        model = "gemini-3.5-flash-lite",
        response_model = Invoice,
        messages = [
            {"role":"user",
             "content":(
                 f"extract content from this text : {text}, and from these tables {tables}"
             )
             }
        ]
    )

