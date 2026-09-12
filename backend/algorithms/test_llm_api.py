import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from backend/.env
load_dotenv()


# Read FreeLLMAPI configuration
api_key = os.getenv("FREELLMAPI_API_KEY")
base_url = os.getenv(
    "FREELLMAPI_BASE_URL",
    "http://localhost:3001/v1"
)


# Make sure the API key exists
if not api_key:
    raise ValueError(
        "FREELLMAPI_API_KEY was not found in backend/.env"
    )


# Create the FreeLLMAPI client
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


# Send a simple test request
response = client.chat.completions.create(
    model="auto",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: LLM connection successful."
        }
    ]
)


# Display the result
print("\n========================================")
print("LLM RESPONSE")
print("========================================")
print(response.choices[0].message.content)
print("========================================")
print("API CONNECTION TEST COMPLETED")
print("========================================")