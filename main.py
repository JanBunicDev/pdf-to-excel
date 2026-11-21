import os
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from repackage import repackaging
from excel import make_excel
import traceback

app = FastAPI()

def cleanup(path):
    if os.path.exists(path):
        os.remove(path)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>PDF -> Excel</h1>
    <p>Click here and press Ctrl+V to paste your PDF</p>
    <div id="paste-box" style="border: 2px dashed #1A3A5C; padding: 40px; text-align: center;">
        Click here, then Ctrl+V your PDF
    </div>
    <p id="status"></p>
    <script>
    const box = document.getElementById('paste-box');
    const status = document.getElementById('status');
    box.tabIndex = 0;
    box.addEventListener('click', () => box.focus());
    box.addEventListener('paste', async (e) => {
        e.preventDefault();
        const files = e.clipboardData.files;
        if (files.length === 0) {
            status.textContent = "No PDF found in clipboard - copy a PDF file first, then Ctrl+V";
            return;
        }
        const file = files[0];
        status.textContent = "Uploading " + file.name + "...";
        const form = new FormData();
        form.append('file', file);
        const res = await fetch('/upload', { method: 'POST', body: form });
        if (!res.ok) {
            const err = await res.text();
            status.textContent = "Error: " + err;
            return;
        }
        const blob = await res.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'invoice.xlsx';
        a.click();
        status.textContent = "Done - Excel downloaded!";
    });
    </script>
    <hr>
    <p>Or old way - browse file:</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".pdf" required>
        <button type="submit">Upload</button>
    </form>
    """

@app.post("/upload")
async def upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    try:
        pdf_path = f"temp_{file.filename}"
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        invoice = repackaging(pdf_path)

        # DELETE PDF RIGHT AFTER WE EXTRACTED IT
        cleanup(pdf_path)

        excel_path = make_excel(invoice)

        # DELETE EXCEL AFTER USER DOWNLOADS IT
        # FileResponse sends it first, then BackgroundTasks deletes it
        background_tasks.add_task(cleanup, excel_path)

        return FileResponse(excel_path, filename="invoice.xlsx")
    except Exception as e:
        print("CRASH:")
        traceback.print_exc()
        # If it crashed, also clean up PDF so it doesn't pile up
        try:
            cleanup(pdf_path)
        except:
            pass
        return JSONResponse({"error": str(e)}, status_code=500)