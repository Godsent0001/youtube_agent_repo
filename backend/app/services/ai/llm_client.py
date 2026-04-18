import requests
from app.core.config import settings


class LLMClient:
    """
    Generic LLM wrapper (Llama 4 / OpenAI-compatible API)
    """

    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = "https://api.llm-provider.com/v1/chat/completions"  # replace

    def generate(self, messages, temperature=0.7):
        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-4-maverick",
                "messages": messages,
                "temperature": temperature
            }
        )

        return response.json()["choices"][0]["message"]["content"]


llm_client = LLMClient()