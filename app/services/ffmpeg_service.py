import os
import subprocess


def extract_audio(video_path: str) -> str:

    audio_path = os.path.splitext(video_path)[0] + ".mp3"

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        audio_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return audio_path