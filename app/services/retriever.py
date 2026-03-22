from typing import List

from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


class Retriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        if not query:
            return []

        query_vector = self.embedding_service.embed([query])
        if not query_vector:
            return []

        results = self.vector_store.search(query_vector[0], top_k)

        chunks: List[str] = []
        for payload in results:
            text = payload.get("text")
            if not isinstance(text, str):
                continue

            source = payload.get("source")
            if isinstance(source, str) and source:
                prefix = f"[source={source}] "
            else:
                prefix = ""

            chunks.append(f"{prefix}{text}")

        return chunks
