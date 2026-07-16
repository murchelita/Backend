from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import media, users,youtube, test, lectures
from app.routers import quiz

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://frontend-note-quiz.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(media.router)
app.include_router(youtube.router)
app.include_router(test.router)

app.include_router(lectures.router)

app.include_router(quiz.router)

@app.get("/")
def read_root():
    return {"Status": "working"}








