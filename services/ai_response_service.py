import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_ai_response(prompt: str):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text