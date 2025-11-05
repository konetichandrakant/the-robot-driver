from openai import OpenAI
from utils.automation_utils import get_model

class LLMService:
    def __init__(self, client:OpenAI):
        self.client = client
        pass

    def generate_response(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=get_model(),
            messages=messages
        )
        return response.choices[0].message.content.strip()