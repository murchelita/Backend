from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import traceback

from app.services.audio_service import (
    save_uploaded_file,
    extract_audio
)

from app.database.database import get_db
from app.database.models import Lecture


router = APIRouter()


@router.post("/api/process-media")
def process_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1. Сохраняем загруженный файл
    try:
        file_info = save_uploaded_file(file)

    except Exception as e:
        print("Error saving file")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"File save failed: {str(e)}"
        )


    # 2. Извлекаем аудио из видео через FFmpeg
    try:
        audio_path = extract_audio(
            file_info["file_path"]
        )

    except Exception as e:
        print("Error extracting audio")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Audio extraction failed: {str(e)}"
        )


    # 3. Создаём запись лекции в базе данных
    try:
        lecture = Lecture(
            id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            source_type="file",
            status="processing"
        )

        db.add(lecture)
        db.commit()
        db.refresh(lecture)

    except Exception as e:
        db.rollback()

        print("Database error")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Database failed: {str(e)}"
        )


    # 4. Ответ API
    return {
        "status": "success",
        "lecture_id": lecture.id,
        "video_path": file_info["file_path"],
        "audio_path": audio_path
    }