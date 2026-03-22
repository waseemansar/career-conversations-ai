import json
from typing import Dict, List

from upstash_redis import Redis

HistoryMessage = Dict[str, str]


class HistoryStore:
    def get(self, session_id: str) -> List[HistoryMessage]:
        raise NotImplementedError

    def set(self, session_id: str, history: List[HistoryMessage]) -> None:
        raise NotImplementedError

    def append(self, session_id: str, role: str, content: str) -> None:
        raise NotImplementedError

    def clear(self, session_id: str) -> None:
        raise NotImplementedError


class RedisHistoryStore(HistoryStore):
    def __init__(
        self,
        client: Redis,
        ttl_seconds: int = 3600,
        max_messages: int = 20,
        prefix: str = "chat:history",
    ):
        self.client = client
        self.ttl_seconds = ttl_seconds
        self.max_messages = max_messages
        self.prefix = prefix

    def _key(self, session_id: str) -> str:
        return f"{self.prefix}:{session_id}"

    def get(self, session_id: str) -> List[HistoryMessage]:
        data = self.client.get(self._key(session_id))

        if not data:
            return []

        if isinstance(data, bytes):
            data = data.decode("utf-8")

        try:
            history = json.loads(data)
            return history if isinstance(history, list) else []
        except json.JSONDecodeError:
            return []

    def set(self, session_id: str, history: List[HistoryMessage]) -> None:
        history = history[-self.max_messages :]

        self.client.set(
            self._key(session_id),
            json.dumps(history),
            ex=self.ttl_seconds,
        )

    def append(self, session_id: str, role: str, content: str) -> None:
        history = self.get(session_id)

        history.append({"role": role, "content": content})

        self.set(session_id, history)

    def clear(self, session_id: str) -> None:
        self.client.delete(self._key(session_id))
