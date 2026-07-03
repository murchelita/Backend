from fastapi import FastAPI
from app.routers import media, users

app = FastAPI()


app.include_router(users.router)
app = FastAPI()

app.include_router(media.router)

@app.get("/")
def root():
    return {"Status": "working"}








