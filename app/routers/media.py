from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import traceback
from app.services.audio_service import (
    save_uploaded_file,
    extract_audio
)
from app.services.whisper_service import (
    transcribe_audio
)
from app.services.gemini_service import (
    generate_summary
)
from app.database.database import get_db
from app.database.models import (
    Lecture,
    User,
    Note,
    Transcript
)


router = APIRouter()



@router.post("/api/process-media")
def process_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):



    #Save uploaded video


    try:

        file_info = save_uploaded_file(file)


    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"File saving failed: {e}"
        )




    #Extract audio using FFmpeg


    try:

        audio_path = extract_audio(
            file_info["file_path"]
        )


    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Audio extraction failed: {e}"
        )




    #Create test user


    user_id = "11111111-1111-1111-1111-111111111111"


    user = db.query(User).filter(
        User.id == user_id
    ).first()



    if not user:

        user = User(

            id=user_id,

            email="test@test.com",

            full_name="Test User"

        )

        db.add(user)

        db.commit()




    #Create lecture


    lecture_id = str(uuid.uuid4())


    try:


        lecture = Lecture(

            id=lecture_id,

            user_id=user_id,

            title=file.filename,

            source_type="file",

            status="processing"

        )


        db.add(lecture)

        db.commit()

        db.refresh(lecture)



    except Exception as e:


        db.rollback()

        traceback.print_exc()


        raise HTTPException(

            status_code=500,

            detail=f"Lecture creation failed: {e}"

        )




    #Speech To Text (Whisper)



    try:


        transcript = transcribe_audio(
            audio_path
        )


    except Exception as e:


        lecture.status = "failed"

        db.commit()


        traceback.print_exc()


        raise HTTPException(

            status_code=500,

            detail=f"Whisper failed: {e}"

        )




    # 6. Generate summary (Gemini)



    try:


        summary = generate_summary(
            transcript
        )


    except Exception as e:


        lecture.status = "failed"

        db.commit()


        traceback.print_exc()


        raise HTTPException(

            status_code=500,

            detail=f"Gemini failed: {e}"

        )




    #Save notes



    try:

        note = Note(

            id=str(uuid.uuid4()),

            lecture_id=lecture.id,

            transcript=transcript,

            summary="",

            key_points=""

        )

        db.add(note)


        lecture.status = "completed"


        db.commit()



    except Exception as e:


        db.rollback()

        traceback.print_exc()


        raise HTTPException(

            status_code=500,

            detail=f"Saving notes failed: {e}"

        )




    #Response



    return {


        "status": "success",


        "lecture_id": lecture.id,


        "video_path": file_info["file_path"],


        "audio_path": audio_path,


        "transcript": transcript,


        "summary": summary

    }