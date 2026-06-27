from fastapi import FastAPI
from app.database.database import engine
app = FastAPI()

@app.get("/")
def root():
    return {"Status":"working"}

@app.get("/db-test")
def db_test():
    try:
        conn = engine.connect()
        conn.close()
        return {"status":"connected"}
    except Exception as e:
        return {"status":"failed"}














