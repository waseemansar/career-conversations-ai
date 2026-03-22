from typing import List, Sequence

from loguru import logger
from openai import OpenAI

from app.config.settings import settings
from app.core.exceptions import OpenAIError


class EmbeddingService:
    def __init__(self, client: OpenAI):
        self.client = client

    def embed(self, texts: Sequence[str]) -> List[List[float]]:
        if not texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=settings.openai_embeddings_model,
                input=list(texts),
            )

            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise OpenAIError() from e
