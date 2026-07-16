#Databases tables (SQLAlchemy)
#import


from sqlalchemy import (
    Column,
    String,
    Text,
    ForeignKey,
    JSON,
    DateTime,
    Integer
)

from sqlalchemy.sql import func
from app.database.database import Base

import uuid



#USERS


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)

    email = Column(
        String,
        unique=True
    )

    full_name = Column(String)




#LECTURES


class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(
        String,
        primary_key=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id")
    )

    title = Column(
        String,
        nullable=False
    )

    source_type = Column(String)

    status = Column(String)

    transcript = Column(Text)


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )




#TRANSCRIPTS


class Transcript(Base):
    __tablename__ = "transcripts"


    id = Column(
        String,
        primary_key=True
    )


    lecture_id = Column(
        String,
        ForeignKey("lectures.id")
    )


    text = Column(Text)


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )




#NOTES


class Note(Base):
    __tablename__ = "notes"

    id = Column(
        String,
        primary_key=True
    )

    lecture_id = Column(
        String,
        ForeignKey("lectures.id")
    )

    summary = Column(Text)

    key_points = Column(Text)


    transcript = Column(Text, nullable=True)




#QUIZZES


class Quiz(Base):
    __tablename__ = "quizzes"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    lecture_id = Column(
        String,
        ForeignKey("lectures.id"),
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )




#QUESTIONS


class Question(Base):
    __tablename__ = "questions"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    quiz_id = Column(
        String,
        ForeignKey("quizzes.id"),
        nullable=False
    )


    question = Column(Text)


    options = Column(JSON)


    answer = Column(Text)




#QUIZ ATTEMPTS


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"


    id = Column(
        String,
        primary_key=True
    )


    user_id = Column(
        String,
        ForeignKey("users.id")
    )


    quiz_id = Column(
        String,
        ForeignKey("quizzes.id")
    )


    score = Column(Integer)


    user_answers = Column(JSON)


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )