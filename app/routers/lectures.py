from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Lecture, Note


router = APIRouter()



@router.get("/api/lectures/{lecture_id}")
def get_lecture(
    lecture_id: str,
    db: Session = Depends(get_db)
):

    lecture = (
        db.query(Lecture)
        .filter(
            Lecture.id == lecture_id
        )
        .first()
    )


    if not lecture:

        raise HTTPException(
            status_code=404,
            detail="Lecture not found"
        )



    note = (
        db.query(Note)
        .filter(
            Note.lecture_id == lecture.id
        )
        .first()
    )



    return {

        "id": lecture.id,

        "title": lecture.title,

        "source_type": lecture.source_type,

        "status": lecture.status,


        "transcript": lecture.transcript,


        "summary":
            note.summary
            if note
            else None,


        "key_points":
            note.key_points
            if note
            else None

    }

@router.get("/api/lectures")
def get_lectures(
    db: Session = Depends(get_db)
):
    lectures = (
        db.query(Lecture)
        .filter(
            Lecture.status == "completed"
        )
        .order_by(
            Lecture.created_at.desc()
        )
        .all()
    )


    return [

        {
            "id": lecture.id,

            "title": lecture.title,

            "source_type": lecture.source_type,

            "status": lecture.status,

            "created_at": lecture.created_at

        }

        for lecture in lectures

    ]