#Databases tables (SQLAlchemy)
#import
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database.database import Base


#users
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    fullname = Column(String)


#lectures
class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))

    source_type = Column(String)
    status = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


#notes
class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True)
    lecture_id = Column(String, ForeignKey("lectures.id"))

    summary = Column(Text)
    key_points = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


#quizzes
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True)
    lecture_id = Column(String, ForeignKey("lectures.id"))

    title = Column(String)


#questions
class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True)
    quiz_id = Column(String, ForeignKey("quizzes.id"))

    question_text = Column(Text)
    options = Column(JSON)
    correct_answer = Column(String)


#quiz attempts
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    quiz_id = Column(String, ForeignKey("quizzes.id"))

    score = Column(Integer)
    user_answers = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())