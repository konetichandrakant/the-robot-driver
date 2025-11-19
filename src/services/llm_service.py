from openai import OpenAI
from src.config import OPENROUTER_MODEL

class LLMService:
    def __init__(self, model: str, client: OpenAI):
        self.model = model
        self.client = client
        pass

    def generate_response(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content.strip()