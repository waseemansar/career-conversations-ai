import uuid


class SessionService:
    @staticmethod
    def get_or_create(session_id: str | None) -> str:
        if session_id:
            return session_id

        return str(uuid.uuid4())
