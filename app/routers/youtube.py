#API for working with Youtube

from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from app.services.youtube_service import download_audio_from_youtube
from app.services.groq_service import transcribe_audio
from app.database.database import get_db

router = APIRouter()

class YoutubeRequest(BaseModel):
    url: str

@router.post("/api/process-youtube")
async def process_media(request: YoutubeRequest):
    try:
        #downloading
        file_info = download_audio_from_youtube(request.url)
        #Groq
        text = transcribe_audio(file_info['file_path'])
        return {"status": "success", "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

