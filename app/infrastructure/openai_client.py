from openai import OpenAI

from app.config.settings import settings

openai = OpenAI(api_key=settings.openai_api_key)
