#API for uploading audio/video files
#import
from fastapi import APIRouter, UploadFile, File

from app.services.audio_service import save_uploaded_file

router = APIRouter()

@router.post("/api/process-media")
def process_media(file: UploadFile = File(...)):
    file_info = save_uploaded_file(file)

    return{
        "status": "success",
        "original_filename": file.filename,
        "saved_as": file_info["safe_filename"],
        "file_path": file_info["file_path"]
    }

