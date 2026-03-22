from fastapi import Request

from app.agents.me_agent import MeAgent
from app.services.history_store import HistoryStore
from app.services.session import SessionService


def get_agent(request: Request) -> MeAgent:
    return request.app.state.agent


def get_history_store(request: Request) -> HistoryStore:
    return request.app.state.history_store


def get_session_service(request: Request) -> SessionService:
    return request.app.state.session_service
