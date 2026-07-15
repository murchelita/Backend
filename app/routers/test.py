from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Lecture, Note, Transcript


router = APIRouter()


@router.get("/api/test-db")
def test_db(db: Session = Depends(get_db)):

    lectures = db.query(Lecture).all()

    result = []

    for lecture in lectures:

        result.append({

            "id": lecture.id,
            "title": lecture.title,
            "status": lecture.status,

        })


    return result