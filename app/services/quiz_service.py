import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise Exception("GROQ_API_KEY missing")


client = Groq(
    api_key=api_key
)



def generate_quiz(text):

    prompt = f"""

Create 5 multiple choice questions from this lecture.

Lecture:

{text}

Return JSON:

{{
 "questions":
 [
   {{
    "question":"",
    "options":[],
    "answer":""
   }}
 ]
}}

"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        response_format={
            "type":"json_object"
        }
    )


    return json.loads(
        response.choices[0].message.content
    )