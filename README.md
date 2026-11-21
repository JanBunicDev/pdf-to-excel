# PDF -> Excel

Paste any invoice PDF, get a clean, pretty Excel in seconds.

No more copy-pasting invoice data by hand.

## Demo

1. Run the app
2. Copy a PDF invoice (Ctrl+C)
3. Click the dashed box, paste (Ctrl+V)
4. Excel downloads automatically

## Features

- Paste PDF with Ctrl+V or upload via file picker
- Extracts text + tables with PyMuPDF
- AI extraction with Gemini + Instructor + Pydantic
- Clean Excel output: Description, Qty, Price, Total
- Auto-calculates TOTAL
- Auto-deletes temp PDF + Excel after download
- English output

## Tech

- Python
- FastAPI + Uvicorn
- PyMuPDF
- Instructor + Gemini 3.5 Flash Lite
- Pydantic
- openpyxl

## Setup

```bash
pip install -r requirements.txt
