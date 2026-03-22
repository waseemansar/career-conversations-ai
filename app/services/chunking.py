from typing import List


# Strategy interface for text chunking.
# Keeps RAGService decoupled from a specific implementation
# so we can swap chunking approaches without modifying core logic.
class ChunkingStrategy:
    def chunk(self, text: str) -> List[str]:
        raise NotImplementedError


class CharacterChunkingStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int = 800, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        if not text:
            return []

        chunks: List[str] = []
        start = 0
        length = len(text)

        while start < length:
            end = min(start + self.chunk_size, length)
            chunks.append(text[start:end])
            if end == length:
                break
            start = max(end - self.overlap, 0)

        return chunks
