#API for uploading audio/video files
#import
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import uuid

from app.services.audio_service import save_uploaded_file
from app.database.database import get_db
from app.database.models import Lecture 
router = APIRouter()

@router.post("/api/process-media")
def process_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_info = save_uploaded_file(file)

    lecture = Lecture(
        id=str(uuid.uuid4()),
        user_id="test-user",  # пока заглушка
        source_type="file",
        status="processing"
    )

    db.add(lecture)
    db.commit()
    db.refresh(lecture)

    return {
        "status": "success",
        "lecture_id": lecture.id,
        "file_path": file_info["file_path"]
    }
