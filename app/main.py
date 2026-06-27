from fastapi import FastAPI
from app.database.database import engine
from app.routers import media
app = FastAPI()

app.include_router(media.router)
@app.get("/")
def root():
    return {"Status":"working"}

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as conn:
              pass
        return {"status":"connected"}
    except Exception as e:
        return {"status":"failed","detail":str(e)}













