from fastapi import APIRouter, UploadFile, File
import shutil, os

from pipeline.pipeline import run_pipeline

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze/")
async def analyze(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_pipeline(file_path)

    return result