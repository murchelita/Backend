from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import media, users,youtube

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://chatty-drivable-unsliced.ngrok-free.dev"
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
@app.get("/")
def read_root():
    return {"Status": "working"}








