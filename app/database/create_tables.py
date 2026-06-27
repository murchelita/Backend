from app.database.database import Base, engine
from app.models.models import User, Lecture, Note, Quiz, Question, QuizAttempt

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("DONE: tables created")