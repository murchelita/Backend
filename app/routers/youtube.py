from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Lecture, Transcript, Note, User

from app.services.youtube_service import download_audio_from_youtube
from app.services.audio_service import compress_audio
from app.services.groq_service import transcribe_audio
from app.services.llm_service import generate_summary


router = APIRouter()


class YoutubeRequest(BaseModel):
    url: str



@router.post("/api/process-youtube")
async def process_youtube(
    request: YoutubeRequest,
    db: Session = Depends(get_db)
):

    try:


        #Download YouTube audio


        file_info = download_audio_from_youtube(
            request.url
        )



        #Compress audio


        compressed_audio = compress_audio(
            file_info["file_path"]
        )



        #Speech To Text


        transcript = transcribe_audio(
            compressed_audio
        )



        #Generate Summary


        summary = generate_summary(
            transcript
        )



        #Тemporary User


        user = db.query(User).first()


        if not user:

            user = User(
                id=str(uuid.uuid4()),
                email="test@example.com",
                full_name="Test User"
            )

            db.add(user)

            db.commit()

            db.refresh(user)




        #Save Lecture


        lecture = Lecture(
            id=str(uuid.uuid4()),

            user_id=user.id,

            title=file_info.get(
                "title",
                "YouTube Lecture"
            ),

            source_type="youtube",

            status="completed",

            transcript=transcript
        )


        db.add(lecture)

        db.commit()

        db.refresh(lecture)




        #Save Transcript


        transcript_db = Transcript(

            id=str(uuid.uuid4()),

            lecture_id=lecture.id,

            text=transcript
        )


        db.add(transcript_db)




        #Save Notes / Summary

        note = Note(

            id=str(uuid.uuid4()),

            lecture_id=lecture.id,

            summary=summary,

            key_points=""
        )


        db.add(note)


        db.commit()




        #Response


        return {

            "status": "success",

            "lecture_id": lecture.id,

            "title": lecture.title,

            "video_url": request.url,

            "audio_path": compressed_audio,

            "transcript": transcript,

            "summary": summary

        }



    except Exception as e:

        db.rollback()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )