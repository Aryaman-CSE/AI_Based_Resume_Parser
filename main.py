from fastapi import FastAPI, UploadFile, File
import pdfplumber
from resume_parser import parse_resume

app = FastAPI(title="AI Resume Parser")

@app.post("/parse-resume")
async def parse_resume_api(file: UploadFile = File(...)):
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return parse_resume(text)
