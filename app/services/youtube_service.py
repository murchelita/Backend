#Downloading audio from Youtube

import os
import uuid
import yt_dlp


UPLOAD_DIR = "uploads"


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


def download_audio_from_youtube(url: str):

    file_id = str(uuid.uuid4())

    output_template = os.path.join(
        UPLOAD_DIR,
        file_id
    )


    ydl_opts = {

        "format": "bestaudio/best",

        "outtmpl": output_template,

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],

        "quiet": False
    }


    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )


        audio_path = output_template + ".mp3"


        if not os.path.exists(audio_path):

            raise Exception(
                f"Audio file not created: {audio_path}"
            )


        return {

            "title": info.get(
                "title",
                "youtube_audio"
            ),

            "file_path": audio_path

        }


    except Exception as e:

        raise Exception(
            f"YouTube download failed: {str(e)}"
        )