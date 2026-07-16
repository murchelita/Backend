import os
import shutil
import subprocess
import uuid
from fastapi import UploadFile


print("FFMPEG PATH:", shutil.which("ffmpeg"))


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
def save_uploaded_file(file: UploadFile) -> dict:

    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )


    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )


    return {
        "file_path": file_path
    }



def extract_audio(video_path: str) -> str:


    filename = os.path.splitext(
        os.path.basename(video_path)
    )[0]


    audio_path = os.path.join(
        UPLOAD_DIR,
        f"processed_{filename}.mp3"
    )


    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        "192k",
        audio_path
    ]


    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    if result.returncode != 0:
        raise Exception(result.stderr)


    return audio_path



def compress_audio(audio_path: str) -> str:


    filename = os.path.splitext(
        os.path.basename(audio_path)
    )[0]


    compressed_path = os.path.join(
        UPLOAD_DIR,
        f"{filename}_compressed.mp3"
    )


    command = [
        "ffmpeg",
        "-y",
        "-i",
        audio_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        "-b:a",
        "64k",
        compressed_path
    ]


    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    if result.returncode != 0:
        raise Exception(result.stderr)


    return compressed_path