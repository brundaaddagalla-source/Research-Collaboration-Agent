import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()


class LLMService:
    """
    Centralized interface for communicating with the LLM
    through FreeLLMAPI.
    """

    def __init__(self):
        self.api_key = os.getenv("FREELLMAPI_API_KEY")

        self.base_url = os.getenv(
            "FREELLMAPI_BASE_URL",
            "http://127.0.0.1:31415/v1"
        )

        if not self.api_key:
            raise ValueError(
                "FREELLMAPI_API_KEY was not found in the .env file."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def generate(
        self,
        prompt: str,
        model: str = "auto"
    ) -> str:
        """
        Send a prompt to the LLM and return the generated text.
        """

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content