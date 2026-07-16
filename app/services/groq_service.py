#Speech recognition via Whisper (Groq)

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY missing")

client = Groq(
    api_key=api_key
)

def transcribe_audio(audio_path: str):

    try:

        with open(audio_path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="text"
            )


        return transcription


    except Exception as e:

        raise Exception(
            f"Whisper transcription failed: {str(e)}"
        )