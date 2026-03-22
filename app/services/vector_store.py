from typing import Any, Dict, List

from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

from app.core.exceptions import QdrantError


# Interface for vector storage operations.
# Allows RAGService to remain independent of a specific
# vector store implementation (e.g., Qdrant).
# Enables swapping providers and easier testing.
class VectorStore:
    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ) -> None:
        raise NotImplementedError

    def search(
        self,
        query_vector: List[float],
        top_k: int,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def clear_collection(self) -> None:
        raise NotImplementedError


class QdrantVectorStore(VectorStore):
    def __init__(self, client: QdrantClient, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    def ensure_collection(self, vector_size: int):
        try:
            collections = self.client.get_collections()
            existing: List[str] = [c.name for c in collections.collections]

            if self.collection_name in existing:
                return

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=rest.VectorParams(
                    size=vector_size,
                    distance=rest.Distance.COSINE,
                ),
            )
        except Exception as e:
            logger.error(f"Failed to ensure collection '{self.collection_name}': {e}")
            raise QdrantError() from e

    def upsert(self, ids, vectors, payloads) -> None:
        if not vectors:
            return

        try:
            self.ensure_collection(vector_size=len(vectors[0]))

            self.client.upsert(
                collection_name=self.collection_name,
                points=rest.Batch.model_construct(
                    ids=ids,
                    vectors=vectors,
                    payloads=payloads,
                ),
            )
        except QdrantError:
            raise
        except Exception as e:
            logger.error(f"Failed to upsert into '{self.collection_name}': {e}")
            raise QdrantError() from e

    def search(self, query_vector, top_k) -> List[Dict[str, Any]]:
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=top_k,
                with_payload=True,
            )

            return [point.payload or {} for point in results.points]
        except Exception as e:
            logger.error(f"Failed to search in '{self.collection_name}': {e}")
            raise QdrantError() from e

    def clear_collection(self) -> None:
        try:
            self.client.delete_collection(collection_name=self.collection_name)
        except Exception as e:
            logger.error(f"Failed to clear collection '{self.collection_name}': {e}")
            raise QdrantError() from e
