import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise Exception("GEMINI_API_KEY missing")


client = genai.Client(
    api_key=api_key
)


def generate_summary(transcript: str):

    prompt = f"""
You are an AI assistant for students.

Based on the lecture transcript, create:

1. A concise summary.
2. The main key points.

Lecture transcript:

{transcript}


Return the answer in this format:

SUMMARY:
...

KEY POINTS:
- ...
- ...
- ...
"""


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )


    return response.text