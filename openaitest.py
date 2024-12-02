import os
import openai
from click import prompt

from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="gpt-4",
  prompt= prompt,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)
