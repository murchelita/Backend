from app.services.groq_service import transcribe_audio


audio_path = "uploads/IMG_5556.mp3"


text = transcribe_audio(audio_path)


print("----- TRANSCRIPT -----")
print(text)