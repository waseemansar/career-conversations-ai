from app.config.settings import settings
from app.infrastructure.openai_client import openai
from app.infrastructure.qdrant_client import client
from app.services.chunking import CharacterChunkingStrategy
from app.services.embeddings import EmbeddingService
from app.services.rag import RAGService
from app.services.retriever import Retriever
from app.services.vector_store import QdrantVectorStore


def build_rag_service() -> RAGService:
    embedding_service = EmbeddingService(client=openai)
    chunking_strategy = CharacterChunkingStrategy()
    vector_store = QdrantVectorStore(client, settings.qdrant_collection_name)
    retriever = Retriever(embedding_service, vector_store)

    return RAGService(
        embedding_service=embedding_service,
        chunking_strategy=chunking_strategy,
        vector_store=vector_store,
        retriever=retriever,
    )
