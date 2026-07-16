from app.database.database import engine, Base
from app.database import models

from sqlalchemy import inspect


print("Deleting old tables...")

Base.metadata.drop_all(bind=engine)


print("Creating tables...")

Base.metadata.create_all(bind=engine)


print("DONE: tables recreated")


inspector = inspect(engine)

print(
    "TABLES:",
    inspector.get_table_names()
)