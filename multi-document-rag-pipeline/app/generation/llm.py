import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, model_name: str, temperature: float = 0.2) -> None:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

        self.client = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=temperature,
        )

    def generate(self, prompt: str) -> str:
        response = self.client.invoke(prompt)
        return str(response.content)

