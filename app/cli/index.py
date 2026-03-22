from app.knowledge.loader import load_documents_for_rag
from app.services.factory import build_rag_service


def main() -> None:
    print("Starting document indexing process...")

    documents = load_documents_for_rag()

    rag = build_rag_service()

    # Clear existing collection before indexing new documents
    rag.clear_collection()

    count = rag.index_documents(documents)
    print(f"Indexed {count} chunks into Qdrant.")


if __name__ == "__main__":
    main()
