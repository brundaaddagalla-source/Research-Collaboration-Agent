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

        # NOTE: we deliberately do NOT raise here anymore.
        # Several agents (ExternalResearcherAgent, PartnershipBriefAgent)
        # construct an LLMService in __init__ even when the caller only
        # wants their non-AI helper methods (e.g. get_candidates()).
        # Raising eagerly meant every route that touched those agents
        # crashed the whole endpoint whenever FREELLMAPI_API_KEY wasn't
        # set, even for plain DB reads. We now raise lazily, only when
        # generate() is actually invoked.
        self.client = (
            OpenAI(api_key=self.api_key, base_url=self.base_url)
            if self.api_key
            else None
        )

    def generate(
        self,
        prompt: str,
        model: str = "auto"
    ) -> str:
        """
        Send a prompt to the LLM and return the generated text.
        """

        if not self.client:
            raise ValueError(
                "FREELLMAPI_API_KEY was not found in the .env file. "
                "Set it in backend/.env to enable AI-generated explanations "
                "and briefs."
            )

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