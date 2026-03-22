from fastapi import APIRouter, Depends

from app.agents.me_agent import MeAgent
from app.core.exceptions import ValidationError
from app.dependencies import get_agent, get_history_store, get_session_service
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.schemas.error_schema import (
    InternalErrorResponse,
    ServiceUnavailableResponse,
    ValidationErrorResponse,
)
from app.services.history_store import HistoryStore
from app.services.session import SessionService

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Send a chat message",
    description="Send a message to the AI agent. Optionally pass a session_id to continue an existing conversation.",
    responses={
        400: {
            "model": ValidationErrorResponse,
            "description": "Invalid or missing field",
        },
        500: {"model": InternalErrorResponse, "description": "Internal server error"},
        503: {
            "model": ServiceUnavailableResponse,
            "description": "Service temporarily unavailable",
        },
    },
)
async def chat(
    request: ChatRequest,
    agent: MeAgent = Depends(get_agent),
    history_store: HistoryStore = Depends(get_history_store),
    session_service: SessionService = Depends(get_session_service),
):
    if not request.message or not request.message.strip():
        raise ValidationError("Message must not be empty")

    session_id = session_service.get_or_create(request.session_id)

    history = history_store.get(session_id)

    response = agent.chat(message=request.message, history=history)

    history_store.append(session_id, "user", request.message)
    history_store.append(session_id, "assistant", response)

    return ChatResponse(session_id=session_id, response=response)
