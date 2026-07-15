from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import (
    Lecture,
    Note,
    Quiz,
    Question
)

from app.services.quiz_service import generate_quiz

import json
import uuid


router = APIRouter()



@router.post("/api/lectures/{lecture_id}/quiz")
def create_quiz(
    lecture_id: str,
    db: Session = Depends(get_db)
):

    # 1.Checking
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



    #summary
    note = (
        db.query(Note)
        .filter(
            Note.lecture_id == lecture.id
        )
        .first()
    )


    if not note:
        raise HTTPException(
            status_code=400,
            detail="No summary found"
        )



    try:

        #AI quiz
        quiz_response = generate_quiz(
            note.summary
        )


        #JSON
        quiz_data = quiz_response


        #Quiz
        new_quiz = Quiz(
            id=str(uuid.uuid4()),
            lecture_id=lecture.id
        )


        db.add(new_quiz)

        db.commit()

        db.refresh(new_quiz)



        #Saving questions
        for item in quiz_data["questions"]:

            question = Question(
                id=str(uuid.uuid4()),

                quiz_id=new_quiz.id,

                question=item["question"],

                options=item["options"],

                answer=item["answer"]
            )


            db.add(question)



        db.commit()



    except Exception as e:

        print(
            "QUIZ ERROR:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



    return {

        "quiz_id": new_quiz.id,

        "lecture_id": lecture_id,

        "questions": quiz_data["questions"]

    }