import os
import shutil
import subprocess
from fastapi import UploadFile


UPLOAD_DIR = "uploads"


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


def save_uploaded_file(file: UploadFile) -> dict: #Save uploaded video file




    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
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


    audio_path = os.path.splitext(video_path)[0] + ".mp3"


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
        raise Exception(
            result.stderr
        )


    return audio_path