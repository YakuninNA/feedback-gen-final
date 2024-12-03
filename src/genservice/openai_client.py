from openai import AsyncOpenAI

from src.config import API_KEY

client = AsyncOpenAI(api_key=API_KEY)
