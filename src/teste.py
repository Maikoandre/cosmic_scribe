from openrouter import OpenRouter
import os
from dotenv import load_dotenv

load_dotenv()

with OpenRouter(
  api_key=os.getenv("OPENROUTER_API_KEY", ""),
) as client:
  response = client.chat.send(
    model="nousresearch/hermes-3-llama-3.1-405b:free",
    messages=[
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  )

  print(response.choices[0].message.content)