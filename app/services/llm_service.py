# app/services/llm_service.py

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


def generate_summary(transcript: str):

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content": """
You are an AI assistant that creates intelligent lecture notes for university students.

Your task:
- Analyze the lecture transcript.
- Extract the most important information.
- Create a structured study guide.

Follow this format:

# Lecture Title

Provide the main topic of the lecture.

# Summary

Write a concise summary of the lecture.

# Main Ideas

List the most important concepts and explanations.

# Key Concepts and Definitions

Explain important terms from the lecture.

# Important Facts

List essential facts, rules, or conclusions.

# Practical Examples

Provide examples if they exist in the transcript.

# Formulas or Technical Details

Include formulas, algorithms, or technical information if applicable.

# Self-Check Questions

Create 10 questions with answers for exam preparation.

Important rules:
- Use only information from the provided transcript.
- Do not invent facts.
- Make the notes clear and easy to study.
"""
                },

                {
                    "role": "user",
                    "content": transcript
                }

            ],

            temperature=0.3,

            max_tokens=4000
        )


        return response.choices[0].message.content


    except Exception as e:

        raise Exception(
            f"Llama generation failed: {str(e)}"
        )