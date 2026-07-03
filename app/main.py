from fastapi import FastAPI
from app.routers import media, users,youtube

app = FastAPI()

app.include_router(users.router)
app.include_router(media.router)
app.include_router(youtube.router)
@app.get("/")
def root():
    return {"Status": "working"}








