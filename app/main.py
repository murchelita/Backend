from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import media, users, youtube, test, lectures, quiz


app = FastAPI()


origins = [
    "http://localhost:5173",
    "https://frontend-note-quiz.vercel.app",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def debug_requests(request: Request, call_next):

    print("METHOD:", request.method)
    print("PATH:", request.url.path)
    print("ORIGIN:", request.headers.get("origin"))

    response = await call_next(request)

    print("STATUS:", response.status_code)

    return response


app.include_router(users.router)
app.include_router(media.router, prefix="/api")
app.include_router(youtube.router)
app.include_router(test.router)
app.include_router(lectures.router)
app.include_router(quiz.router)


@app.get("/")
def read_root():
    return {
        "Status": "working"
    }