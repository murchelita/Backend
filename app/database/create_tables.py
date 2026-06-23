from app.database.database import Base, engine
from app.database.models import *

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("DONE: tables created")