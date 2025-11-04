import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env.example")

class LLMService:
    def __init__(self, client:OpenAI):
        self.client = client
        pass

    def generate_response(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL"),
            messages=messages
        )
        return response.choices[0].message.content.strip()