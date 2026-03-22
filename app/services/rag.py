import uuid
from collections.abc import Iterable
from typing import Any, Dict, List, TypedDict

from app.services.chunking import ChunkingStrategy
from app.services.embeddings import EmbeddingService
from app.services.retriever import Retriever
from app.services.vector_store import VectorStore


class DocumentForIndex(TypedDict):
    id: str
    text: str
    source: str
    metadata: Dict[str, Any]


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        chunking_strategy: ChunkingStrategy,
        vector_store: VectorStore,
        retriever: Retriever,
    ):
        self.embedding_service = embedding_service
        self.chunking_strategy = chunking_strategy
        self.vector_store = vector_store
        self.retriever = retriever

    def index_documents(self, documents: Iterable[DocumentForIndex]) -> int:
        docs = list(documents)
        if not docs:
            return 0

        all_chunks: List[str] = []
        ids: List[str] = []
        payloads: List[Dict[str, Any]] = []

        for doc in docs:
            chunks = self.chunking_strategy.chunk(doc["text"])
            for i, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                ids.append(chunk_id)
                all_chunks.append(chunk)
                payloads.append(
                    {
                        "source": doc["source"],
                        "text": chunk,
                        **doc.get("metadata", {}),
                    }
                )

        vectors = self.embedding_service.embed(all_chunks)
        self.vector_store.upsert(ids, vectors, payloads)

        return len(ids)

    def clear_collection(self) -> None:
        self.vector_store.clear_collection()

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        return self.retriever.retrieve(query, top_k)
